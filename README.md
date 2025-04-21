# 💸 Expense Tracker - Tkinter Desktop App

A beginner-friendly personal finance manager written in Python. This app helps users **log income/expenses**, **visualize trends**, and **export data to Excel**, all through a clean GUI built using Tkinter.

---

## ✨ Features

✅ User Authentication (Login & Signup)  
✅ Add Income & Expense Transactions  
✅ View Full Transaction History  
✅ Visualize Spending & Income via Charts  
✅ Export Data to Excel (`.xlsx` format)

---

## 🛠️ Technologies Used

- **Frontend**: Tkinter (Python GUI)
- **Backend**: SQLite (Lightweight Database)
- **Data Analysis**: Pandas  
- **Charts**: Matplotlib

---

## 🗃️ Database Design

### `User` Table
| Column   | Type    | Description                    |
|----------|---------|--------------------------------|
| id       | INTEGER | Primary key                    |
| username | TEXT    | Unique                         |
| password | TEXT    | Plaintext (⚠️ not secure)     |

### `Expenses` Table
| Column     | Type    | Description                   |
|------------|---------|-------------------------------|
| id         | INTEGER | Primary key                   |
| user_id    | INTEGER | Foreign key (User.id)         |
| amount     | REAL    | Expense amount                |
| category   | TEXT    | e.g. Food, Rent               |
| description| TEXT    | Optional notes                |
| date       | TEXT    | Format: YYYY-MM-DD            |

### `Income` Table
| Column  | Type    | Description                     |
|---------|---------|---------------------------------|
| id      | INTEGER | Primary key                     |
| user_id | INTEGER | Foreign key (User.id)           |
| amount  | REAL    | Income amount                   |
| source  | TEXT    | e.g. Salary, Freelance          |
| date    | TEXT    | Format: YYYY-MM-DD              |

---

## 📈 System Workflow

1. **User Signup/Login**  
2. **Add Transactions** (Income/Expense)  
3. **View History**  
4. **Generate Charts** (Category-wise or Source-wise)  
5. **Export to Excel**

---

## 🚧 Security Notes

> 🔐 Passwords are currently stored as plaintext.  
> You can improve this by hashing passwords using libraries like `bcrypt`.

---

## ✅ To-Do (Future Improvements)

- [ ] Encrypt passwords using hashing
- [ ] Add date filtering in visualizations
- [ ] Add monthly/weekly summary dashboard

---

## 📸 Screenshots (optional)

*You can add screenshots or GIFs of your app in action inside the `assets/` folder.*

---

## 🧠 Made with 💻 by Muhammad Taha (Tee)

DATABASE SYSTEMS | FAST NUCES - PESHAWAR CAMPUS | 23P-0559
