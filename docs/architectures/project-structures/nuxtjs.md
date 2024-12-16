my-nuxt-app/
├── .nuxt/                      # Auto-generated build directory
│                              # Contains compiled app, components, types
├── .output/                    # Production build output
│                              # Contains optimized server/client bundles
├── .nitro/                     # Nitro server build
│                              # Contains server middleware and handlers
│
├── assets/                     # Build-processed assets
│   ├── css/                   # Global styles
│   │   ├── main.scss         # Main styles
│   │   ├── variables.scss    # SCSS variables
│   │   └── themes/           # Theme files
│   │       ├── light.scss    # Light theme
│   │       └── dark.scss     # Dark theme
│   ├── images/               # Images for processing
│   │   ├── icons/           # Icon files
│   │   │   └── sprite/      # SVG sprites
│   │   └── backgrounds/     # Background images
│   └── fonts/               # Font files
│       └── custom/          # Custom fonts
│
├── components/               # Vue components (auto-imported)
│   ├── base/                # Base/atomic components
│   │   ├── BaseButton.vue  # <BaseButton />
│   │   ├── BaseInput.vue   # <BaseInput />
│   │   └── BaseCard.vue    # <BaseCard />
│   ├── forms/              # Form components
│   │   ├── LoginForm.vue   # <LoginForm />
│   │   └── SearchForm.vue  # <SearchForm />
│   ├── layout/             # Layout components
│   │   ├── TheHeader.vue  # <TheHeader />
│   │   ├── TheFooter.vue  # <TheFooter />
│   │   └── TheSidebar.vue # <TheSidebar />
│   ├── modals/            # Modal/dialog components
│   │   ├── ConfirmModal.vue # <ConfirmModal />
│   │   └── AlertModal.vue   # <AlertModal />
│   └── ui/                # Feature components
│       ├── UserCard.vue   # Regular component
│       └── UserProfile.island.vue # Island component
│
├── composables/            # Vue composables (auto-imported)
│   ├── states/            # State management
│   │   ├── useAuth.ts     # Authentication
│   │   └── useUser.ts     # User state
│   ├── features/          # Feature logic
│   │   ├── useSearch.ts   # Search
│   │   ├── useCart.ts     # Shopping cart
│   │   └── usePagination.ts # Pagination
│   └── utils/             # Utility composables
│       ├── useFetch.ts    # API fetching
│       └── useForm.ts     # Form handling
│
├── content/               # Content management
│   ├── blog/             # Blog content
│   │   └── posts/       # Blog posts
│   └── docs/            # Documentation
│       ├── api/         # API docs
│       ├── setup/       # Setup guides
│       └── security/    # Security docs
│
├── layouts/              # Page layouts
│   ├── default.vue      # Default layout
│   ├── admin.vue        # Admin layout
│   └── auth.vue         # Auth layout
│
├── middleware/           # Route middleware
│   ├── auth.ts          # Auth checks
│   ├── admin.ts         # Admin access
│   └── analytics.global.ts # Global tracking
│
├── pages/               # File-based routing
│   ├── index.vue       # Home (/)
│   ├── about.vue       # About (/about)
│   ├── admin/         # Admin pages
│   │   ├── index.vue  # Dashboard
│   │   └── users.vue  # User management
│   └── users/         # User routes
│       ├── index.vue  # List
│       ├── [id].vue   # Profile
│       ├── [[status]].vue # Optional param
│       └── [...slug].vue # Catch-all
│
├── plugins/            # App plugins
│   ├── api.ts         # API client
│   ├── auth.ts        # Authentication
│   ├── error-handler.ts # Error handling
│   ├── analytics.client.ts # Analytics
│   ├── performance.client.ts # Performance
│   └── websocket.server.ts # WebSockets
│
├── public/             # Static files
│   ├── favicon.ico    # Favicon
│   ├── robots.txt     # SEO rules
│   ├── security.txt   # Security policy
│   ├── images/        # Static images
│   └── files/         # Downloads
│
├── server/            # Server-side code
│   ├── api/          # API endpoints
│   │   ├── auth/     # Auth endpoints
│   │   │   ├── login.post.ts
│   │   │   ├── logout.post.ts
│   │   │   ├── refresh.post.ts
│   │   │   └── register.post.ts
│   │   ├── users/    # User endpoints
│   │   │   ├── index.get.ts
│   │   │   ├── [id].get.ts
│   │   │   └── [id].patch.ts
│   │   └── webhooks/ # Webhook handlers
│   │       └── stripe.post.ts
│   ├── middleware/   # Server middleware
│   │   ├── auth.ts  # Authentication
│   │   ├── cors.ts  # CORS handling
│   │   ├── rate-limit.ts # Rate limiting
│   │   ├── security.ts # Security headers
│   │   └── compression.ts # Compression
│   ├── plugins/     # Server plugins
│   │   ├── database.ts # Database
│   │   ├── cache.ts # Cache
│   │   └── socket.ts # WebSockets
│   └── utils/      # Server utilities
│       ├── database/ # DB utilities
│       │   ├── queries.ts
│       │   └── models.ts
│       ├── auth/   # Auth utilities
│       │   ├── jwt.ts
│       │   └── crypto.ts
│       ├── cache/  # Caching
│       │   ├── redis.ts
│       │   └── memory.ts
│       ├── email/  # Email handling
│       │   └── templates.ts
│       ├── queue/  # Job queues
│       │   └── processor.ts
│       ├── logger/ # Logging
│       │   └── winston.ts
│       ├── monitoring/ # Monitoring
│       │   └── metrics.ts
│       ├── performance/ # Performance
│       │   └── metrics.ts
│       ├── security/ # Security
│       │   ├── encryption.ts
│       │   └── sanitization.ts
│       └── validation/ # Validation
│           └── schemas.ts
│
├── shared/           # Universal code
│   └── utils/       # Shared utilities
│       ├── datetime.ts
│       └── validation.ts
│
├── types/           # TypeScript types
│   ├── api.d.ts    # API types
│   ├── env.d.ts    # Environment types
│   ├── config.d.ts # Config types
│   ├── components.d.ts # Component types
│   ├── plugins.d.ts # Plugin types
│   ├── global.d.ts # Global types
│   └── models.d.ts # Data models
│
├── test/            # Testing
│   ├── unit/       # Unit tests
│   │   ├── components/
│   │   ├── composables/
│   │   └── utils/
│   ├── integration/ # Integration tests
│   │   └── api/
│   └── e2e/       # E2E tests
│       └── features/
│
├── .env            # Dev environment variables
├── .env.example    # Environment template
├── .gitignore      # Git ignore patterns
├── app.vue         # Root Vue component
├── app.config.ts   # Runtime config
├── error.vue       # Error page
├── nuxt.config.ts  # Nuxt configuration
├── package.json    # Project dependencies
├── tsconfig.json   # TypeScript config
└── README.md       # Project documentation

Special Patterns:
- *.client.*  - Client-only
- *.server.*  - Server-only
- *.global.*  - Global middleware
- *.island.*  - Island components
- [param]     - Required parameter
- [[param]]   - Optional parameter
- [...slug]   - Catch-all routes

Key Features:
1. Security
   - CSP headers
   - Rate limiting
   - CORS policies
   - Input validation
   - Authentication
   - Authorization
   - Data sanitization

2. Performance
   - Caching
   - Compression
   - Asset optimization
   - Code splitting
   - Island components

3. Development
   - Type safety
   - Error handling
   - Testing coverage
   - Documentation
   - Code organization
  