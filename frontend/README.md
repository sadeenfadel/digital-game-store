# Frontend - Digital Game Store

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

The default configuration:

```env
VITE_API_BASE_URL=/api
```

This uses the Vite dev server proxy (`vite.config.ts`) to forward all `/api` requests to the Flask backend at `http://localhost:5000`. This means the backend URL does not need to be hardcoded and there are no CORS issues in development.

### 3. Start the Backend

Start the Flask backend in a separate terminal first (see `backend/README.md`):

```bash
cd ../backend && source venv/bin/activate && flask run
```

### 4. Start the Frontend

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/              # Reusable UI components
│   │   ├── Header/              # Navigation bar with logout
│   │   ├── ProductCard/         # Product display card
│   │   ├── Pagination/          # Pagination controls
│   │   ├── LocationFilter/      # JO/SA filter buttons
│   │   ├── LoadingSpinner/      # Loading indicator
│   │   ├── ErrorMessage/        # Error display with retry
│   │   └── ProtectedRoute/      # Route authentication guard
│   ├── pages/                   # Application screens
│   │   ├── LoginPage/           # Authentication page
│   │   ├── ProductsPage/        # Product listing (grid, filter, pagination)
│   │   ├── ProductDetailsPage/  # Product details + buy button
│   │   └── ReceiptPage/         # Order confirmation receipt
│   ├── services/                # API communication layer
│   │   ├── apiClient.ts         # Centralized Axios client with JWT interceptor
│   │   ├── authService.ts       # POST /auth/login
│   │   ├── productService.ts    # GET /products, GET /products/:id
│   │   └── orderService.ts      # POST /orders, GET /orders/:id
│   ├── models/                  # TypeScript interfaces (API contracts)
│   │   ├── user.ts
│   │   ├── product.ts
│   │   ├── order.ts
│   │   └── error.ts
│   ├── context/                 # React contexts
│   │   └── AuthContext.tsx       # Authentication state (token, user, login/logout)
│   ├── hooks/                   # Custom React hooks
│   │   └── useAuth.ts
│   ├── routes/                  # Route definitions
│   │   └── AppRoutes.tsx
│   ├── utils/                   # Utility functions
│   │   └── storage.ts           # localStorage helpers
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global responsive stylesheet
├── public/                      # Static assets
├── package.json                 # Dependencies
├── vite.config.ts               # Vite config + API proxy
├── tsconfig.json                # TypeScript configuration
└── .env.example                 # Environment variables template
```

## Routes

| Path | Component | Protected |
|------|-----------|-----------|
| `/login` | LoginPage | No |
| `/products` | ProductsPage | Yes |
| `/products/:id` | ProductDetailsPage | Yes |
| `/receipt/:id` | ReceiptPage | Yes |

## Build

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Backend API Dependency

This frontend requires the Flask backend running at `http://localhost:5000`.

During development, the Vite proxy (`vite.config.ts`) forwards `/api` requests from the frontend dev server (port 5173) to the backend (port 5000).

## Dependencies

- **React 18**: UI framework
- **React Router 6**: Client-side routing
- **Axios**: HTTP client (centralized in `apiClient.ts` with JWT interceptor)
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
