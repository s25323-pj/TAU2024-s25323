## **Opis projektu**
Projekt polega na stworzeniu planszy o wymiarach `AxB` z:
- Punktem startowym **START**, oznaczonym jako **A**.
- Punktem końcowym **STOP**, oznaczonym jako **B**.
- Przeszkodami oznaczonymi jako **X**.

Celem jest generowanie planszy i implementacja podstawowych ruchów na planszy zgodnie z zasadami:
1. Poruszanie się w czterech kierunkach: góra, dół, lewo, prawo.
2. Unikanie przeszkód.
3. Nie wychodzenie poza granice planszy.

---

## **Funkcjonalności**

### **1. Losowanie START i STOP**
- START i STOP znajdują się na krawędziach planszy.
- START i STOP są w różnych miejscach i nie są obok siebie.

### **2. Generowanie przeszkód**
- Przeszkody są rozmieszczane losowo na planszy.
- Nie mogą zajmować miejsc START ani STOP.

### **3. Ruch na planszy**
- Możliwość ruchu w czterech kierunkach:
  - **up** (góra)
  - **down** (dół)
  - **left** (lewo)
  - **right** (prawo)
- Logika ruchu sprawdza:
  - Czy ruch nie prowadzi poza granice planszy.
  - Czy ruch nie prowadzi na przeszkodę.

### **4. Eksport do pliku**
- Plansza oraz ścieżka (**Path**) są zapisywane w pliku `board.txt`.

### **5. Testy jednostkowe**
- Testy sprawdzają poprawność ruchów, w tym przypadki brzegowe:
  - Ruch na pole z przeszkodą.
  - Próba wyjścia poza granice planszy.

### **6. GitHub Actions**
- Workflow automatycznie uruchamia testy przy każdym pushu do repozytorium.

