# 💰 Virtual Wallet - Digital Payment System

A robust and secure RESTful API for a digital wallet system built with Django and Django REST Framework. This application enables users to manage their digital wallets, perform peer-to-peer transfers, and track transaction history with a complete audit trail.

---

## 🚀 Features

### ✅ User Management
- User registration with automatic wallet creation
- JWT-based authentication (access & refresh tokens)
- Secure password validation
- User profile management

### ✅ Wallet Management
- Automatic wallet creation on user registration
- Unique account number generation
- Real-time balance tracking
- Multi-currency support (NGN default)

### ✅ Transaction System
- **Peer-to-peer transfers** between users
- Transaction status tracking (PENDING, COMPLETED, FAILED)
- Unique transaction reference generation
- Transaction history with filtering

### ✅ Ledger System
- Double-entry bookkeeping
- Complete audit trail for all transactions
- Debit and credit tracking
- Immutable ledger entries

### ✅ Security Features
- JWT authentication
- Password hashing
- CORS configuration
- Environment-based configuration
- Protected endpoints

---

## 🛠️ Tech Stack

- **Backend Framework:** Django 4.2.7
- **API Framework:** Django REST Framework 3.14.0
- **Authentication:** Simple JWT 5.3.0
- **Database:** 
  - SQLite (Development)
  - PostgreSQL (Production)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Environment Management:** Python Decouple

---

## 📋 Prerequisites

- Python 3.13.8+
- pip (Python package manager)
- Git
- Virtual environment (recommended)

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/virtual_wallet.git
cd virtual_wallet
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOW_ALL_ORIGINS=True
```

Generate a secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register/` | Register new user | No |
| POST | `/api/v1/auth/login/` | Login user | No |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token | No |

### Wallet Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/wallet/` | Get user wallet details | Yes |
| GET | `/api/v1/wallet/balance/` | Get wallet balance | Yes |

### Transaction Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/transactions/transfer/` | Transfer money to another user | Yes |
| GET | `/api/v1/transactions/` | Get transaction history | Yes |
| GET | `/api/v1/transactions/{id}/` | Get specific transaction | Yes |

---

## 🔐 API Usage Examples

### 1. Register a New User

```bash
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "wallet": {
    "account_number": "1234567890",
    "balance": "0.00",
    "currency": "NGN"
  }
}
```

### 2. Login

```bash
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Get Wallet Balance

```bash
GET /api/v1/wallet/balance/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "balance": "50000.00",
  "currency": "NGN"
}
```

### 4. Transfer Money

```bash
POST /api/v1/transactions/transfer/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "recipient_username": "janedoe",
  "amount": "5000.00",
  "description": "Payment for services"
}
```

**Response:**
```json
{
  "id": 1,
  "transaction_type": "TRANSFER_OUT",
  "amount": "5000.00",
  "status": "COMPLETED",
  "reference": "TXN_TRA_1234567890",
  "description": "Payment for services",
  "recipient": "janedoe",
  "created_at": "2025-10-23T10:30:00Z",
  "balance_after": "45000.00"
}
```

### 5. Get Transaction History

```bash
GET /api/v1/transactions/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "transaction_type": "TRANSFER_OUT",
      "amount": "5000.00",
      "status": "COMPLETED",
      "reference": "TXN_TRA_1234567890",
      "created_at": "2025-10-23T10:30:00Z"
    }
  ]
}
```

---

## 🗂️ Project Structure

```
virtual_wallet/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── users/                 # User management app
│   ├── models.py          # User models
│   ├── serializers.py     # User serializers
│   └── views.py           # User views
├── wallets/               # Wallet management app
│   ├── models.py          # Wallet models
│   ├── serializers.py     # Wallet serializers
│   └── views.py           # Wallet views
├── transactions/          # Transaction management app
│   ├── models.py          # Transaction models
│   ├── serializers.py     # Transaction serializers
│   └── views.py           # Transaction views
├── ledger/                # Ledger/audit trail app
│   ├── models.py          # Ledger models
│   └── services.py        # Ledger services
├── payments/              # Payment processing app
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment configuration
├── runtime.txt            # Python version
└── .env.example           # Environment variables template
```

---

## 🚀 Deployment

### Deploy to Railway

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add PostgreSQL database
   - Set environment variables:
     ```
     SECRET_KEY=your-production-secret-key
     DEBUG=False
     ALLOWED_HOSTS=.railway.app,.up.railway.app
     CORS_ALLOW_ALL_ORIGINS=True
     ```

3. **Railway will automatically:**
   - Install dependencies
   - Run migrations
   - Start the server

Your API will be live at: `https://your-app.railway.app`

---

## 🧪 Testing

### Run Tests

```bash
python manage.py test
```

### Test with API Clients

- **Postman:** Import the API endpoints and test
- **Thunder Client:** VS Code extension for API testing
- **curl:** Command-line testing

---

## 📊 Database Schema

### Users
- Standard Django User model
- One-to-one relationship with Wallet

### Wallets
- `user` (ForeignKey to User)
- `account_number` (Unique, 10 digits)
- `balance` (Decimal)
- `currency` (CharField, default: NGN)

### Transactions
- `wallet` (ForeignKey to Wallet)
- `transaction_type` (DEPOSIT, WITHDRAWAL, TRANSFER_IN, TRANSFER_OUT)
- `amount` (Decimal)
- `status` (PENDING, COMPLETED, FAILED)
- `reference` (Unique transaction ID)
- `description` (Optional)

### Ledger Entries
- Double-entry bookkeeping
- Links to transactions
- Immutable audit trail

---

## 🔒 Security Considerations

- ✅ JWT tokens expire after 15 minutes (configurable)
- ✅ Refresh tokens valid for 7 days
- ✅ Passwords hashed with Django's default hasher
- ✅ CORS configured for production
- ✅ Environment variables for sensitive data
- ✅ SQL injection protection (Django ORM)
- ✅ CSRF protection enabled

---

## 🛣️ Roadmap

- [ ] Add deposit functionality (payment gateway integration)
- [ ] Add withdrawal to bank accounts
- [ ] Implement webhooks for async notifications
- [ ] Add transaction filtering by date/type/status
- [ ] Admin dashboard for reporting
- [ ] Email notifications for transactions
- [ ] Two-factor authentication (2FA)
- [ ] Rate limiting for API endpoints
- [ ] Mobile app integration

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Simple JWT
- Railway for hosting
- All contributors and testers

---

## 📞 Support

For support, email your.email@example.com or create an issue in the GitHub repository.

---

## 🔗 Links

- **Live API:** https://your-app.railway.app
- **Documentation:** https://your-app.railway.app/api/docs/
- **GitHub:** https://github.com/yourusername/virtual_wallet

---

**Built with ❤️ using Django & Django REST Framework**
