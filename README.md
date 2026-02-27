# Lavender Chatter

A modern chat application built with React, TypeScript, and Supabase.

## Features

- Real-time chat interface
- AI-powered responses
- Clean and responsive UI with Tailwind CSS
- Built with modern React patterns

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite
- **UI Components**: shadcn/ui, Radix UI
- **Styling**: Tailwind CSS
- **Backend**: Supabase
- **State Management**: TanStack Query

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Supabase account (for backend services)

### Installation

1. Clone the repository:
```sh
git clone <your-repo-url>
cd lavender-chatter
```

2. Install dependencies:
```sh
npm install
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials:
     - `VITE_SUPABASE_URL`
     - `VITE_SUPABASE_PUBLISHABLE_KEY`
     - `VITE_SUPABASE_PROJECT_ID`

4. Start the development server:
```sh
npm run dev
```

The app will be available at `http://localhost:8080`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run build:dev` - Build in development mode
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
lavender-chatter/
├── src/
│   ├── components/     # React components
│   ├── hooks/          # Custom React hooks
│   ├── integrations/   # Third-party integrations
│   ├── lib/            # Utility functions
│   ├── pages/          # Page components
│   └── types/          # TypeScript type definitions
├── supabase/           # Supabase functions
└── public/             # Static assets
```

## Deployment

Build the project for production:

```sh
npm run build
```

The built files will be in the `dist` directory, ready to be deployed to any static hosting service.

## License

MIT
