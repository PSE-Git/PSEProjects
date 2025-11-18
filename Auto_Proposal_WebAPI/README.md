# Auto Proposal WebAPI

A FastAPI-based web API for generating and managing business proposals, with support for Google Cloud SQL and PDF generation.

## Features

- Client management (CRUD operations)
- Proposal generation and management
- PDF generation with ReportLab
- Google Cloud SQL support (MySQL/PostgreSQL)
- REST API endpoints
- Automatic PDF generation and storage

## Project Structure

```
/src
  /auto_proposal
    /api           # FastAPI routes and endpoints
    /core         # Core business logic, models, schemas
    /db           # Database connectivity and repositories
    /services     # Business services (PDF generation, etc.)
/tests           # Unit and integration tests
```

## Setup Instructions

1. Create Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run database migrations:
```bash
python -m src.auto_proposal.db.database
```

5. Run the application:
```bash
uvicorn src.auto_proposal.api.main:app --reload
```

## Google Cloud SQL Setup

### Local Development (Cloud SQL Auth Proxy)

1. Install Cloud SQL Auth Proxy:
   - Download from: https://cloud.google.com/sql/docs/mysql/sql-proxy
   - Add to PATH

2. Start the proxy:
```bash
./cloud_sql_proxy -instances=PROJECT:REGION:INSTANCE=tcp:3306
```

3. Configure database connection:
```
# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/auto_proposal

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/auto_proposal
```

### Production Setup

1. Create a Google Cloud SQL instance (MySQL or PostgreSQL)
2. Configure network access (private IP or authorized networks)
3. Update DATABASE_URL with production credentials

## API Endpoints

### Clients
- `POST /api/clients` - Create client
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client
- `GET /api/clients/{id}` - Get client details

### Proposals
- `POST /api/proposals` - Create proposal
- `PUT /api/proposals/{id}` - Update proposal
- `DELETE /api/proposals/{id}` - Delete proposal
- `GET /api/proposals/{id}` - Get proposal details
- `POST /api/proposals/{id}/pdf` - Generate PDF
- `GET /api/proposals/{id}/pdf` - Download PDF

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.