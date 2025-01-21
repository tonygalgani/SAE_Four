#include "MAX31856.h"
#include "mbed.h"

#define K  1.5
#define TD 30.0
#define TI 45.0

#define TE 1.0  //Periode echantillonage
#define T 1.0   //Periode globale

PwmOut Ventilo(D9);
PwmOut Chauffage(D7);

SPI spi(A6, A5, A4);            // A6 = Entree_esclave(SDI)(MOSI);  A5 = Sortie_Esclave(SDO)(MISO); clock = A4
MAX31856 Thermocouple(spi, D0); // Chip select = D0

const static float Tableau_consigne_pate[18][3] = {
    // {Temps(t) ,Température_de_depart(b), Pente correspondante(a)}
    { 23,  25,  2.04},     
    { 48,  72,  1.60},   
    { 72, 112,  1.04},  
    { 90, 137,  0.72},
    {121, 150,  0.32},
    {159, 160,  0.21}, 
    {180, 168,  0.33}, 
    {189, 175,  1.11},
    {202, 185,  1.54}, 
    {210, 205,  1.50}, 
    {218, 217,  1.63}, 
    {231, 230,  1.15},
    {240, 245,  0.44},
    {252, 249, -0.42},
    {256, 244, -0.75},
    {264, 241, -1.63},
    {270, 228, -1.83}};

int main() {
    wait(5); //Delay for logs

    int i = 0, rc = 0.0;
    float erreur_temperature = 0.0, erreur_temperature_pred = 0.0, temps = 0, temps_pente = 0, aw=1;
    float Temp_Consigne, Temperature_TC;

    float vi, vd, vc;
    float vi_pred = 0, vd_pred = 0;

    Ventilo.period(T);
    Chauffage.period(T);

    Ventilo.pulsewidth(0);
    Chauffage.pulsewidth(0);
    
    // printf("temps Temp_Consigne Temperature_TC erreur_temperature rc");
    
    while (temps < 300) {

        while (temps < Tableau_consigne_pate[i][0]) {
            
            Temp_Consigne = Tableau_consigne_pate[i][2] * temps_pente + Tableau_consigne_pate[i][1];  //Calcul Temperature de Consigne
            Temperature_TC = Thermocouple.readTC();     //Lecture temperature four
            erreur_temperature = Temp_Consigne - Temperature_TC;     //Calcul de l'erreur
            
            vi = vi_pred + aw * (TE/TI)*erreur_temperature ;
            vd = ( 1 / ( 1 + 0.1*(TD/TE) ) ) 
                *( 0.1*( TD/TE ) * vd_pred +( TD/TE )*(erreur_temperature-erreur_temperature_pred) );

            vc = K * (erreur_temperature + vi + vd);

            if (temps <= 270){

                //Commande du chauffage                
                if (vc < 0.0){
                    Chauffage.pulsewidth(0);
                    aw = 0;
                }
                if (vc > 100.0){
                    Chauffage.pulsewidth(1);
                    aw=0;
                }
                else{
                    Chauffage.pulsewidth(vc / 100 * T);
                    aw=1;
                }
            }
            if(temps > 270){
                //Fin du Chauffage
                Chauffage.pulsewidth(0);
                //Refroidissement
                Ventilo.pulsewidth(0.6);
            }

            //Envoie des donnees par liaison serie
            printf("%hu %hu %hu %hu \n", (uint16_t)(temps*10), (uint16_t)(Temp_Consigne*10), (uint16_t)(Temperature_TC*10), (uint16_t)(vc));
            //printf("%f\n\r",vc);
            temps += TE;
            temps_pente += TE;
            wait(T);

            vd_pred = vd;
            vi_pred = vi;
            erreur_temperature_pred = erreur_temperature;
        }
        i++;
        temps_pente = 0;
    }
    //Fin du Ventilateur
    Ventilo.pulsewidth(0);    
}
