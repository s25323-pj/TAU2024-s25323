package com.example.tau_4;

import com.example.tau_4.exceptions.PaymentFailedException;
import com.example.tau_4.exceptions.ProductNotAvailableException;
import com.example.tau_4.model.Order;
import com.example.tau_4.model.PaymentResult;
import com.example.tau_4.service.InventoryService;
import com.example.tau_4.service.NotificationService;
import com.example.tau_4.service.OrderService;
import com.example.tau_4.service.PaymentService;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Tau4Application {

    public static void main(String[] args) {
        InventoryService inventoryService = new InventoryService() {
            @Override
            public boolean isAvailable(String product, int quantity) {
                return product.equalsIgnoreCase("Laptop") && quantity <= 10;
            }
        };

        PaymentService paymentService = new PaymentService() {
            @Override
            public PaymentResult processPayment(double amount) {
                if (amount > 0 && amount < 5000) {
                    return new PaymentResult(true, "Płatność zakończona sukcesem.");
                }
                return new PaymentResult(false, "Brak środków.");
            }
        };

        NotificationService notificationService = new NotificationService() {
            @Override
            public void notifyUser(String user, String message) {
                System.out.println("Powiadomienie dla " + user + ": " + message);
            }
        };

        OrderService orderService = new OrderService(paymentService, inventoryService, notificationService);

        Order order = new Order("jan.kowalski", "Laptop", 1, 3999.99);

        try {
            System.out.println("Próba składania zamówienia...");
            orderService.placeOrder(order);
            System.out.println("Zamówienie zostało pomyślnie złożone!");
        } catch (ProductNotAvailableException e) {
            System.err.println("Błąd: " + e.getMessage());
        } catch (PaymentFailedException e) {
            System.err.println("Błąd: " + e.getMessage());
        }
    }
}

