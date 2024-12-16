my-nuxt-app/
├── .nuxt/                      # Auto-generated build directory
│                              # Dev-time compilation, types, and registry
├── .output/                    # Production build output
│                              # Optimized assets and server/client bundles
├── .nitro/                     # Nitro server build
│                              # Server routes, middleware, and cache
│
├── assets/                     # Processed by build tools
│   ├── css/                   
│   │   ├── main.scss          # Main stylesheet
│   │   ├── variables.scss     # SCSS variables/mixins
│   │   └── themes/            # Theme variations
│   │       ├── light.scss
│   │       └── dark.scss
│   ├── images/               
│   │   ├── icons/            # SVG/icon assets
│   │   │   └── sprite/       # SVG sprite icons
│   │   └── backgrounds/      # Background images
│   └── fonts/                # Web fonts
│       └── custom/           # Custom font files
│
├── components/                # Vue components (auto-imported)
│   ├── base/                 # Atomic/base components
│   │   ├── BaseButton.vue   # <BaseButton />
│   │   ├── BaseInput.vue    # <BaseInput />
│   │   └── BaseCard.vue     # <BaseCard />
│   ├── forms/               # Form components
│   │   ├── LoginForm.vue    # <LoginForm />
│   │   └── SearchForm.vue   # <SearchForm />
│   ├── layout/              # Layout components
│   │   ├── TheHeader.vue   # <TheHeader />
│   │   ├── TheFooter.vue   # <TheFooter />
│   │   └── TheSidebar.vue  # <TheSidebar />
│   ├── modals/             # Modal dialogs
│   │   ├── ConfirmModal.vue # <ConfirmModal />
│   │   └── AlertModal.vue  # <AlertModal />
│   └── ui/                 # Feature components
│       ├── UserCard.vue    # Regular component
│       └── UserProfile.island.vue # Island component
│
├── composables/             # Composition utilities
│   ├── states/             # State management
│   │   ├── useAuth.ts      # Authentication state
│   │   └── useUser.ts      # User state
│   ├── features/           # Feature logic
│   │   ├── useSearch.ts    # Search functionality
│   │   ├── useCart.ts      # Shopping cart
│   │   └── usePagination.ts # Pagination logic
│   └── utils/              # Utility composables
│       ├── useFetch.ts     # Enhanced fetching
│       └── useForm.ts      # Form handling
│
├── content/                # Content management
│   ├── blog/              # Blog posts
│   │   └── posts/        # Post files
│   └── docs/             # Documentation
│       └── api/          # API docs
│
├── layouts/               # Page layouts
│   ├── default.vue       # Default layout
│   ├── admin.vue         # Admin layout
│   └── auth.vue          # Auth layout
│
├── middleware/            # Route middleware
│   ├── auth.ts           # Auth checks
│   ├── admin.ts          # Admin guards
│   └── analytics.global.ts # Global tracking
│
├── pages/                 # File-based routing
│   ├── index.vue         # Home (/)
│   ├── about.vue         # About (/about)
│   ├── admin/           # Admin pages
│   │   ├── index.vue    # Dashboard
│   │   └── users.vue    # User management
│   └── users/           # User pages
│       ├── index.vue    # List (/users)
│       ├── [id].vue     # Profile (/users/123)
│       ├── [[status]].vue # Optional (/users/active?)
│       └── [...slug].vue # Catch-all
│
├── plugins/              # App plugins
│   ├── api.ts           # API setup
│   ├── auth.ts          # Auth setup
│   ├── analytics.client.ts # Client analytics
│   └── websocket.server.ts # Server websockets
│
├── public/               # Static assets
│   ├── favicon.ico      # Favicon
│   ├── robots.txt       # SEO rules
│   ├── security.txt     # Security policy
│   ├── images/          # Static images
│   └── files/           # Downloads
│
├── server/              # Server-side code
│   ├── api/            # API endpoints
│   │   ├── auth/       # Auth endpoints
│   │   │   ├── login.post.ts
│   │   │   ├── logout.post.ts
│   │   │   ├── refresh.post.ts
│   │   │   └── register.post.ts
│   │   └── users/      # User endpoints
│   │       ├── index.get.ts
│   │       ├── [id].get.ts
│   │       └── [id].patch.ts
│   ├── middleware/     # Server middleware
│   │   ├── auth.ts    # Auth verification
│   │   ├── cors.ts    # CORS policies
│   │   ├── rate-limit.ts # Rate limiting
│   │   └── security.ts # Security headers
│   ├── plugins/       # Server plugins
│   │   ├── database.ts # DB connection
│   │   ├── cache.ts   # Cache setup
│   │   └── socket.ts  # WebSocket
│   └── utils/        # Server utilities
│       ├── database/ # DB helpers
│       │   ├── queries.ts
│       │   └── models.ts
│       ├── auth/     # Auth utils
│       │   ├── jwt.ts
│       │   └── crypto.ts
│       ├── cache/    # Cache utils
│       │   ├── redis.ts
│       │   └── memory.ts
│       ├── monitoring/
│       │   └── metrics.ts
│       ├── security/
│       │   └── encryption.ts
│       ├── types/    # Type defs
│       │   └── models.ts
│       └── validation/
│           └── schemas.ts
│
├── shared/             # Universal code
│   └── utils/         # Shared utilities
│       ├── datetime.ts
│       └── validation.ts
│
├── types/             # TypeScript types
│   ├── api.ts        # API types
│   └── models.ts     # Data models
│
├── utils/             # Client utilities
│   ├── formatting.ts  # Formatters
│   ├── validation.ts  # Validators
│   └── helpers.ts     # General utils
│
├── test/              # Test files
│   ├── unit/         # Unit tests
│   │   ├── components/
│   │   └── composables/
│   └── e2e/          # E2E tests
│       └── specs/
│
├── .env              # Dev env vars
├── .env.example      # Env template
├── .gitignore        # Git ignore
├── app.vue           # Root component
├── app.config.ts     # Runtime config
├── error.vue         # Error page
├── nuxt.config.ts    # Nuxt config
├── package.json      # Dependencies
├── tsconfig.json     # TS config
└── README.md         # Documentation

Key Notes:

1. File Patterns:
   - *.client.* - Client-only
   - *.server.* - Server-only
   - *.global.* - Global middleware
   - *.island.* - Island components
   - [param] - Required param
   - [[param]] - Optional param
   - [...slug] - Catch-all

2. Security:
   - Use HTTPS in production
   - Implement rate limiting
   - Set security headers
   - Sanitize inputs
   - Validate data
   - Handle CORS properly
   - Use secure sessions
   - Implement proper auth flow

3. Best Practices:
   - Single root element
   - Async middleware
   - Proper type definitions
   - Error handling
   - Environment config
   - API documentation