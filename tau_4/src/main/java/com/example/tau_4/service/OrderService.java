package com.example.tau_4.service;

import com.example.tau_4.exceptions.PaymentFailedException;
import com.example.tau_4.exceptions.ProductNotAvailableException;
import com.example.tau_4.model.Order;
import com.example.tau_4.model.PaymentResult;

public class OrderService {

    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    public OrderService(PaymentService paymentService,
                        InventoryService inventoryService,
                        NotificationService notificationService) {
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
        this.notificationService = notificationService;
    }

    public void placeOrder(Order order) {
        boolean available = inventoryService.isAvailable(order.product(), order.quantity());
        if (!available) {
            throw new ProductNotAvailableException("Produkt " + order.product() + " jest niedostępny.");
        }

        PaymentResult paymentResult;
        try {
            paymentResult = paymentService.processPayment(order.amount());
        } catch (Exception e) {
            throw new PaymentFailedException("Wystąpił błąd podczas przetwarzania płatności: " + e.getMessage());
        }

        if (!paymentResult.success()) {
            throw new PaymentFailedException("Płatność nie powiodła się: " + paymentResult.message());
        }

        notificationService.notifyUser(order.user(), "Twoje zamówienie zostało złożone pomyślnie!");
    }
}
