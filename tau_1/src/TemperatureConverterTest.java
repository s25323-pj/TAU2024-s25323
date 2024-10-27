import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TemperatureConverterTest {

    @Test
    void testCelsiusToFahrenheit() {
        assertEquals(32.0, TemperatureConverter.celsiusToFahrenheit(0), 0.01);
    }

    @Test
    void testFahrenheitToCelsius() {
        assertEquals(0.0, TemperatureConverter.fahrenheitToCelsius(32), 0.01);
    }

    @Test
    void testCelsiusToKelvin() {
        assertEquals(273.15, TemperatureConverter.celsiusToKelvin(0), 0.01);
    }

    @Test
    void testKelvinToCelsius() {
        assertEquals(0.0, TemperatureConverter.kelvinToCelsius(273.15), 0.01);
    }

    @Test
    void testFahrenheitToKelvin() {
        assertEquals(273.15, TemperatureConverter.fahrenheitToKelvin(32), 0.01);
    }

    @Test
    void testKelvinToFahrenheit() {
        assertEquals(32.0, TemperatureConverter.kelvinToFahrenheit(273.15), 0.01);
    }

    @Test
    void testInvalidKelvinInput() {
        assertThrows(IllegalArgumentException.class, () -> TemperatureConverter.kelvinToCelsius(-1));
    }

    @Test
    void testNonZeroCelsiusToFahrenheit() {
        assertNotEquals(0.0, TemperatureConverter.celsiusToFahrenheit(25), 0.01);
    }

    @Test
    void testLargeFahrenheitToKelvin() {
        double result = TemperatureConverter.fahrenheitToKelvin(1000);
        assertTrue(result > 500, "Expected result to be greater than 500");
    }

    @Test
    void testSmallKelvinToFahrenheit() {
        double result = TemperatureConverter.kelvinToFahrenheit(0.1);
        assertEquals(-459.67, result, 0.2, "Expected result to be approximately -459.67");
    }
}
