# Lavender Chatter - Setup Guide

## What Changed

Your project has been transformed from a Lovable template into your own custom chat application with a service-based interface.

### Key Changes Made:

1. **Removed Lovable Dependencies**
   - Removed `lovable-tagger` package
   - Cleaned up Lovable API references
   - Updated README with generic instructions

2. **New Service-Based Interface**
   - Replaced chat history sidebar with service boxes
   - Added 8 service categories:
     - Government Schemes
     - Healthcare
     - Gmail Assistant
     - Calendar
     - Education & Scholarships
     - Financial Services
     - Housing Schemes
     - Employment & Skills

3. **Service-Specific AI Context**
   - Each service has its own system prompt
   - AI responses are tailored to the selected service
   - Welcome messages are customized per service

## Project Structure

```
lavender-chatter/
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── ServiceGrid.tsx      # NEW: Service selection sidebar
│   │       ├── ChatScreen.tsx       # Updated with service context
│   │       └── ...
│   ├── types/
│   │   ├── service.ts               # NEW: Service definitions
│   │   └── chat.ts
│   └── pages/
│       └── Index.tsx                # Updated to use ServiceGrid
└── supabase/
    └── functions/
        └── chat/
            └── index.ts             # Updated to handle service context
```

## Running the Project

The development server is already running at:
- **Local**: http://localhost:8080/
- **Network**: http://10.17.24.106:8080/

### Commands:
```bash
npm run dev      # Start development server (already running)
npm run build    # Build for production
npm run preview  # Preview production build
```

## Next Steps

### 1. Set Up Supabase (Required for AI Chat)

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Copy your credentials to `.env`:
   ```env
   VITE_SUPABASE_PROJECT_ID="your-project-id"
   VITE_SUPABASE_PUBLISHABLE_KEY="your-anon-key"
   VITE_SUPABASE_URL="https://your-project.supabase.co"
   ```

### 2. Configure AI API (Required for Chat Functionality)

The chat function needs an AI API. Options:

**Option A: OpenAI**
1. Get API key from https://platform.openai.com
2. In Supabase Dashboard → Edge Functions → Secrets, add:
   - `AI_API_KEY`: Your OpenAI API key
   - `AI_API_URL`: `https://api.openai.com/v1/chat/completions`

**Option B: Google Gemini**
1. Get API key from https://makersuite.google.com/app/apikey
2. Update `supabase/functions/chat/index.ts` to use Gemini format
3. Add secrets in Supabase

**Option C: Anthropic Claude**
1. Get API key from https://console.anthropic.com
2. Update the function accordingly

### 3. Deploy Supabase Function

```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link your project
supabase link --project-ref your-project-id

# Deploy the function
supabase functions deploy chat
```

### 4. Add Real Integrations (Optional)

To make Gmail, Calendar, etc. actually work:

1. **Gmail Integration**
   - Use Gmail API
   - Add OAuth authentication
   - Update service handler in chat function

2. **Calendar Integration**
   - Use Google Calendar API
   - Implement event creation/management

3. **Government Schemes**
   - Integrate with official APIs if available
   - Add database of schemes

## Customization

### Add New Services

Edit `src/types/service.ts`:

```typescript
{
  id: 'my-service',
  name: 'My Service',
  description: 'Service description',
  icon: 'IconName', // From lucide-react
  color: 'from-color-500 to-color-600',
  category: 'productivity',
  systemPrompt: 'You are a helpful assistant for...'
}
```

### Modify Service Colors/Icons

Available icons from lucide-react: https://lucide.dev/icons/
Update the `iconMap` in `ServiceGrid.tsx` if adding new icons.

### Change Theme

Edit `src/index.css` to modify the lavender color scheme.

## Current Status

✅ Project cleaned of Lovable references
✅ Service-based interface implemented
✅ Development server running
✅ TypeScript compilation successful
⚠️ Supabase credentials needed (using placeholder)
⚠️ AI API configuration needed for chat to work

## Troubleshooting

**Chat not working?**
- Check Supabase credentials in `.env`
- Verify AI API key is set in Supabase secrets
- Check browser console for errors

**Services not showing?**
- Clear browser cache
- Check console for errors
- Verify all imports are correct

**Build errors?**
- Run `npm install` to ensure all dependencies are installed
- Check TypeScript errors with `npm run lint`
