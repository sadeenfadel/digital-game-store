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

Edit `.env` if needed:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ProductCard/     # Product display card
│   │   ├── Pagination/      # Pagination controls
│   │   └── ProtectedRoute/  # Route authentication guard
│   ├── pages/               # Application screens
│   │   ├── LoginPage/       # Authentication page
│   │   ├── ProductsPage/    # Product listing
│   │   ├── ProductDetailsPage/ # Product details
│   │   └── ReceiptPage/     # Order receipt
│   ├── services/            # API communication
│   │   ├── apiClient.ts     # Centralized Axios client
│   │   ├── authService.ts   # Authentication API
│   │   ├── productService.ts # Products API
│   │   └── orderService.ts  # Orders API
│   ├── models/              # TypeScript interfaces
│   ├── context/             # React contexts
│   │   └── AuthContext.tsx   # Authentication state
│   ├── hooks/               # Custom React hooks
│   │   └── useAuth.ts       # Auth hook
│   ├── routes/              # Route definitions
│   │   └── AppRoutes.tsx    # Application routes
│   ├── utils/               # Utility functions
│   │   └── storage.ts       # Local storage helpers
│   ├── App.tsx              # Root component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── package.json             # Dependencies
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
└── .env.example             # Environment variables template
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

This frontend requires the backend API to be running at the URL specified in `VITE_API_BASE_URL`.

## Dependencies

- **React 18**: UI framework
- **React Router 6**: Client-side routing
- **Axios**: HTTP client
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
