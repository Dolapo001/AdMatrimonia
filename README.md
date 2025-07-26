# AdMatrimonia

AdMatrimonia is a comprehensive platform that combines event advertising and matrimonial services. It allows users to post event ads, create matrimonial profiles, and connect with diverse people in their community.

## 🚀 Features

### Event Advertising
- **Multi-Category Ads**: Support for 15+ categories including matrimony, events, services, property, automotive, jobs, and more
- **Advanced Search & Filtering**: Search by location, category, price range, and keywords
- **Favorites System**: Save and manage favorite ads
- **User Dashboard**: Manage your posted ads with status tracking
- **Image Support**: Upload multiple images for each ad

### Matrimonial Services
- **Detailed Profiles**: Create comprehensive matrimonial profiles with personal information
- **Photo Gallery**: Upload and manage multiple profile pictures
- **Partner Preferences**: Set detailed preferences for potential matches
- **Connection System**: Send and receive connection requests
- **Bookmark Profiles**: Save interesting profiles for later review
- **Real-time Messaging**: Chat with connections (via WebSocket)

### Core Features
- **JWT Authentication**: Secure user authentication and authorization
- **RESTful API**: Well-documented API with OpenAPI/Swagger documentation
- **Admin Dashboard**: Beautiful Jazzmin-powered admin interface
- **Search History**: Track user search patterns
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: WebSocket support for live notifications

## 🛠️ Technology Stack

### Backend
- **Django 5.2.3**: Modern Python web framework
- **Django REST Framework**: Powerful API development
- **Django Channels**: WebSocket support for real-time features
- **PostgreSQL/SQLite**: Database support
- **Redis**: Caching and WebSocket message broker
- **Celery**: Background task processing
- **JWT**: Token-based authentication

### Frontend Integration Ready
- **OpenAPI/Swagger**: Auto-generated API documentation
- **CORS Support**: Ready for frontend integration
- **RESTful Design**: Clean API endpoints

## 📋 Prerequisites

- Python 3.8+
- Redis Server
- PostgreSQL (optional, SQLite included for development)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AdMatrimonia.git
cd AdMatrimonia
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - SQLite is default)
DATABASE_URL=postgresql://user:password@localhost:5432/admatrimonia

# Redis (required for Channels)
REDIS_URL=redis://localhost:6379/0

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Seed Categories (Optional)
```bash
python manage.py seed_categories
```

### 7. Start Redis Server
```bash
redis-server
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

### 9. Start Celery Worker (Optional)
```bash
celery -A AdMatrimonia worker -l info
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/user/register/` - User registration
- `POST /api/v1/user/login/` - User login
- `POST /api/v1/user/forgot-password/` - Password reset request
- `POST /api/v1/user/reset-password/` - Password reset confirmation

### Ads Management
- `GET /api/v1/ads/ads/` - List all ads (with filtering)
- `POST /api/v1/ads/create/` - Create new ad
- `GET /api/v1/ads/{id}/` - Get ad details
- `GET /api/v1/ads/user/` - Get user's ads
- `GET /api/v1/ads/category_list/` - List categories
- `GET /api/v1/ads/sub_category_list/` - List subcategories

### Favorites
- `GET /api/v1/ads/favorites/` - List favorite ads
- `POST /api/v1/ads/{id}/favorite/` - Add to favorites
- `DELETE /api/v1/ads/{id}/unfavorite/` - Remove from favorites

### Matrimonial Profiles
- `GET /api/v1/matrimony/profile/` - Get user profile
- `POST /api/v1/matrimony/profile/create/` - Create profile
- `PUT /api/v1/matrimony/profile/update/` - Update profile
- `DELETE /api/v1/matrimony/profile/delete/` - Delete profile
- `GET /api/v1/matrimony/profiles/` - List all profiles
- `GET /api/v1/matrimony/profiles/{user_id}/` - Get specific profile

### Profile Pictures
- `POST /api/v1/matrimony/profile/pictures/` - Upload picture
- `GET /api/v1/matrimony/profile/{user_id}/pictures/` - Get profile pictures
- `DELETE /api/v1/matrimony/profile/pictures/{picture_id}/` - Delete picture

### Partner Preferences
- `GET /api/v1/matrimony/preferences/` - Get preferences
- `POST /api/v1/matrimony/preferences/create/` - Create preferences
- `PUT /api/v1/matrimony/preferences/update/` - Update preferences

### Connections
- `POST /api/v1/matrimony/connections/send/` - Send connection request
- `GET /api/v1/matrimony/connections/received/` - Get received requests
- `GET /api/v1/matrimony/connections/sent/` - Get sent requests
- `POST /api/v1/matrimony/connections/respond/` - Respond to request

### Bookmarks
- `GET /api/v1/matrimony/bookmarks/` - List bookmarks
- `POST /api/v1/matrimony/bookmarks/toggle/` - Toggle bookmark

## 🏗️ Project Structure

```
AdMatrimonia/
├── AdMatrimonia/           # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL configuration
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
├── ads/                   # Ads management app
│   ├── models.py          # Ad, Category, SubCategory models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   └── constants.py       # Category constants
├── matrimonial/           # Matrimonial services app
│   ├── models.py          # Profile, Connection models
│   ├── views.py           # API views
│   └── serializers.py     # DRF serializers
├── core/                  # User management app
│   ├── models.py          # Custom User model
│   ├── views.py           # Authentication views
│   └── serializers.py     # Auth serializers
├── common/                # Shared utilities
│   ├── models.py          # Base model
│   ├── response_managers.py # Response utilities
│   └── utils.py           # Helper functions
├── chat/                  # Real-time chat app
│   ├── models.py          # Chat models
│   ├── consumers.py       # WebSocket consumers
│   └── routing.py         # WebSocket routing
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Categories Supported
- Matrimony Services
- Events & Entertainment
- Professional Services
- Property & Real Estate
- Automotive
- Items for Sale
- Jobs & Employment
- Lifestyle & Social
- Travel & Tourism
- Wedding Services
- And more...

### Real-time Features
- Live chat between connected users
- Real-time notifications
- Connection request updates
- New message alerts

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📦 Deployment

### Production Settings
1. Set `DEBUG=False` in environment
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for production
4. Configure email settings
5. Set up static file serving
6. Configure CORS for frontend domain

### Docker Support (Coming Soon)
Docker configuration will be added for easy deployment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@admatrimonia.com

## 🚧 Roadmap

- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced matching algorithm
- [ ] Video calling integration
- [ ] Payment gateway integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Social media integration

---

**AdMatrimonia** - Connecting Communities, Creating Opportunities