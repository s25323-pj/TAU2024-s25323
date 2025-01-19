package com.example.tau_4.service;

import com.example.tau_4.model.PaymentResult;



public interface PaymentService {
    PaymentResult processPayment(double amount);
}