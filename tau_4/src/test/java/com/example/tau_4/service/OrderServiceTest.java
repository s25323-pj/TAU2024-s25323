package com.example.tau_4.service;

import com.example.tau_4.exceptions.PaymentFailedException;
import com.example.tau_4.exceptions.ProductNotAvailableException;
import com.example.tau_4.model.Order;
import com.example.tau_4.model.PaymentResult;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class OrderServiceTest {

    private PaymentService paymentService;
    private InventoryService inventoryService;
    private NotificationService notificationService;

    private OrderService orderService;

    @BeforeEach
    void setUp() {
        paymentService = Mockito.mock(PaymentService.class);
        inventoryService = Mockito.mock(InventoryService.class);
        notificationService = Mockito.mock(NotificationService.class);

        orderService = new OrderService(paymentService, inventoryService, notificationService);
    }

    @Test
    void placeOrder_WhenAllIsOk() {
        Order order = new Order("jan.kowalski", "Laptop", 1, 3999.99);

        when(inventoryService.isAvailable("Laptop", 1)).thenReturn(true);

        when(paymentService.processPayment(3999.99))
                .thenReturn(new PaymentResult(true, "OK"));

        orderService.placeOrder(order);

        verify(inventoryService, times(1))
                .isAvailable("Laptop", 1);

        verify(paymentService, times(1))
                .processPayment(3999.99);

        verify(notificationService, times(1))
                .notifyUser("jan.kowalski", "Twoje zamówienie zostało złożone pomyślnie!");
    }


    @Test
    void placeOrder_WhenProductNotAvailable() {
        Order order = new Order("jan.kowalski", "Smartphone", 2, 2999.99);

        when(inventoryService.isAvailable("Smartphone", 2)).thenReturn(false);

        assertThrows(ProductNotAvailableException.class, () -> orderService.placeOrder(order));

        verify(paymentService, never()).processPayment(anyDouble());
        verify(notificationService, never()).notifyUser(anyString(), anyString());
    }


    @Test
    void placeOrder_WhenPaymentFails() {
        Order order = new Order("anna.nowak", "TV", 1, 2999.0);

        when(inventoryService.isAvailable("TV", 1)).thenReturn(true);

        when(paymentService.processPayment(2999.0))
                .thenReturn(new PaymentResult(false, "Brak środków na koncie"));

        assertThrows(PaymentFailedException.class, () -> orderService.placeOrder(order));

        verify(paymentService, times(1)).processPayment(2999.0);
        verify(notificationService, never()).notifyUser(anyString(), anyString());
    }


    @Test
    void placeOrder_WhenPaymentServiceThrowsException() {

        Order order = new Order("adam.kowalski", "Konsola", 1, 1999.0);

        when(inventoryService.isAvailable("Konsola", 1)).thenReturn(true);

        when(paymentService.processPayment(1999.0))
                .thenThrow(new RuntimeException("Błąd zewnętrznego systemu płatności"));

        assertThrows(PaymentFailedException.class, () -> orderService.placeOrder(order));

        verify(notificationService, never()).notifyUser(anyString(), anyString());
    }
}