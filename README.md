# Payment Gateway System

A comprehensive Django REST API-based payment gateway system with Razorpay integration, featuring user authentication, product management, and secure payment processing.

## Features

- **User Authentication System**
  - User registration and login
  - Admin user creation
  - JWT token-based authentication
  - Custom user model with UUID primary keys

- **Product Management**
  - CRUD operations for products
  - Image upload support for product images
  - Product listing and detailed views
  - Admin panel integration

- **Payment Processing**
  - Razorpay integration for secure payments
  - Order creation and payment verification
  - Transaction tracking and status management
  - Payment signature verification

- **API Documentation**
  - Swagger/OpenAPI documentation
  - Interactive API testing interface
  - Comprehensive endpoint documentation

## Technology Stack

- **Backend Framework**: Django 5.1.5
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Payment Gateway**: Razorpay
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **CORS**: django-cors-headers
- **Environment Management**: python-decouple

## Project Structure

```
payment_gateway/
├── manage.py
├── payment_gateway/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── user/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── products/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Razorpay Account (for payment processing)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd payment_gateway
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install drf-yasg
pip install razorpay
pip install python-decouple
pip install psycopg2-binary
pip install djangorestframework-simplejwt
pip install pillow
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# Django Settings
DJANGO_SETTINGS_MODULE=payment_gateway.settings.local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Razorpay Configuration
RAZOR_KEY_ID=your_razorpay_key_id
RAZOR_KEY_SECRET=your_razorpay_key_secret
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /token/` - Obtain JWT tokens
- `POST /token/refresh/` - Refresh JWT token
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/register/admin/` - Admin registration
- `GET /api/user/` - Get authenticated user info

### Products

- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT/PATCH /api/products/{id}/` - Update product (Auth required)
- `DELETE /api/products/{id}/` - Delete product (Auth required)

### Payments

- `POST /api/create-order/` - Create Razorpay order
- `POST /api/verify-payment/` - Verify payment signature

### Documentation

- `GET /api/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation

## Models

### User Model
- Custom user model extending AbstractBaseUser
- UUID primary key
- JWT token generation method
- Username and email authentication

### Products Model
- UUID primary key
- Name, price, description fields
- Image upload functionality
- Timestamps for creation and updates

### Transactions Model
- UUID primary key
- Order ID and payment ID tracking
- Amount and status fields
- Integration with Razorpay orders

## Payment Flow

1. **Create Order**: Frontend calls `/api/create-order/` with amount
2. **Razorpay Integration**: Order created in Razorpay and database
3. **Payment Processing**: User completes payment through Razorpay
4. **Verification**: Frontend calls `/api/verify-payment/` with payment details
5. **Status Update**: Transaction status updated to "Paid"

## Environment-Specific Settings

The project supports multiple environments:

- **Local Development**: `payment_gateway.settings.local`
- **Development**: `payment_gateway.settings.dev`
- **Production**: `payment_gateway.settings.prod`

Configure the `DJANGO_SETTINGS_MODULE` environment variable accordingly.

## Security Features

- JWT token authentication with configurable expiry
- CORS configuration for frontend integration
- CSRF protection
- Password validation
- Secure payment signature verification

## CORS Configuration

Currently configured to allow requests from:
- `http://localhost:5173` (typical Vite/React dev server)

Modify `CORS_ALLOWED_ORIGINS` in settings for production use.

## Admin Panel

Access the Django admin panel at `/admin/` with superuser credentials:
- User management with custom admin interface
- Product management with image previews
- Transaction monitoring

## Testing

Run tests using Django's test framework:

```bash
python manage.py test
```

## Deployment Considerations

1. **Environment Variables**: Ensure all sensitive data is in environment variables
2. **Database**: Use PostgreSQL in production
3. **Static Files**: Configure static file serving for production
4. **CORS**: Update CORS settings for production domains
5. **Debug**: Set `DEBUG=False` in production
6. **Secret Key**: Use a secure secret key in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions, please create an issue in the repository or contact the development team.
