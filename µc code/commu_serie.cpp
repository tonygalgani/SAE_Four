#include "mbed.h"
#include <cstdint>

#define WAIT_TIME_MS 500

int main() {

    float temps = 0;
    float temperature;
    float commandeChauffage;

  while(true) {
    temps = 1071;
    temperature = 250.5;
    commandeChauffage = 50.5;

    printf("%hu %hu %hu \n\r", (uint16_t)(temps), (uint16_t)(temperature * 10), (uint16_t)(commandeChauffage * 10));

    wait_ms(WAIT_TIME_MS);
  }
}
