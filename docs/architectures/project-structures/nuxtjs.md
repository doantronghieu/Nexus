my-nuxt-app/
├── .nuxt/                      # Auto-generated build directory - Never modify manually
│                              # Contains compiled app, types, and component registry
├── .output/                    # Production build output directory
│                              # Contains optimized server/client bundles and assets 
├── .nitro/                     # Nitro server build output and cache
│                              # Contains server middleware, routes, and handlers
│
├── assets/                     # Assets processed by build tools (Vite/Webpack)
│   ├── css/                   # Global styles and preprocessor files
│   │   ├── main.scss         # Main stylesheet (processed by preprocessor)
│   │   ├── variables.scss    # Shared variables and mixins
│   │   └── themes/           # Theme-specific styles
│   ├── images/               # Images for optimization/transformation
│   │   ├── icons/           # SVG and icon assets
│   │   └── backgrounds/      # Background images
│   └── fonts/               # Web fonts to be included in bundle
│       └── custom/          # Custom font files
│
├── components/               # Vue components (auto-imported by name)
│   ├── base/                # Atomic/base components
│   │   ├── BaseButton.vue  # Basic button -> <BaseButton />
│   │   ├── BaseInput.vue   # Basic input -> <BaseInput />
│   │   └── BaseCard.vue    # Basic card -> <BaseCard />
│   ├── forms/              # Form-specific components
│   │   ├── LoginForm.vue   # Login form -> <LoginForm />
│   │   └── SearchForm.vue  # Search form -> <SearchForm />
│   ├── layout/             # Layout/structural components
│   │   ├── TheHeader.vue  # Main header -> <TheHeader />
│   │   ├── TheFooter.vue  # Main footer -> <TheFooter />
│   │   └── TheSidebar.vue # Sidebar -> <TheSidebar />
│   ├── modals/            # Modal/dialog components
│   │   ├── ConfirmModal.vue # Confirmation -> <ConfirmModal />
│   │   └── AlertModal.vue   # Alerts -> <AlertModal />
│   └── ui/                 # Complex UI and features
│       ├── UserCard.vue    # Regular component -> <UserCard />
│       └── UserProfile.island.vue # Island component -> <UserProfile />
│
├── composables/             # Reusable Vue composables (auto-imported)
│   ├── states/             # State management composables
│   │   ├── useAuth.ts     # Authentication state -> useAuth()
│   │   └── useUser.ts     # User state -> useUser()
│   ├── features/          # Feature-specific composables
│   │   ├── useSearch.ts   # Search functionality -> useSearch()
│   │   └── useCart.ts     # Shopping cart -> useCart()
│   └── utils/             # Utility composables
│       ├── useFetch.ts    # Enhanced fetch -> useFetch()
│       └── useForm.ts     # Form handling -> useForm()
│
├── content/                 # File-based CMS (requires @nuxt/content)
│   ├── blog/              # Blog posts in Markdown/MDX
│   │   └── posts/        # Blog post files
│   └── docs/              # Documentation files
│       └── api/          # API documentation
│
├── layouts/                # Page layouts (require single root element)
│   ├── default.vue        # Default layout (auto-applied)
│   ├── admin.vue          # Admin layout
│   └── auth.vue           # Authentication layout
│
├── middleware/             # Navigation middleware (route guards)
│   ├── auth.ts            # Authentication checks
│   ├── admin.ts           # Admin area protection
│   └── analytics.global.ts # Global tracking (runs on all routes)
│
├── pages/                  # File-based routing (auto-generated)
│   ├── index.vue          # Home page (/)
│   ├── about.vue          # About page (/about)
│   ├── admin/            # Admin section (/admin/*)
│   │   ├── index.vue     # Admin dashboard
│   │   └── users.vue     # User management
│   └── users/            # User routes
│       ├── index.vue     # Users list (/users)
│       ├── [id].vue      # User profile (/users/123)
│       ├── [[status]].vue # Optional status (/users/active?)
│       └── [...slug].vue # Catch-all user routes
│
├── plugins/               # App plugins (initialization)
│   ├── api.ts            # API client setup
│   ├── auth.ts           # Authentication
│   ├── analytics.client.ts # Client-only analytics
│   └── websocket.server.ts # Server-only websockets
│
├── public/                # Static files (served at root)
│   ├── favicon.ico       # Browser favicon
│   ├── robots.txt        # SEO instructions
│   ├── images/           # Static images
│   └── files/            # Downloadable files
│
├── server/               # Server-side code
│   ├── api/             # API endpoints
│   │   ├── auth/        # Authentication endpoints
│   │   │   ├── login.post.ts    # POST /api/auth/login
│   │   │   ├── logout.post.ts   # POST /api/auth/logout
│   │   │   └── register.post.ts # POST /api/auth/register
│   │   └── users/       # User endpoints
│   │       ├── index.get.ts     # GET /api/users
│   │       ├── [id].get.ts      # GET /api/users/:id
│   │       └── [id].patch.ts    # PATCH /api/users/:id
│   ├── middleware/      # Server middleware
│   │   ├── auth.ts     # Authentication verification
│   │   ├── cors.ts     # CORS handling
│   │   ├── rate-limit.ts # Rate limiting
│   │   └── security.ts # Security headers
│   ├── plugins/        # Nitro server plugins
│   │   ├── database.ts # Database connection
│   │   ├── cache.ts    # Cache initialization
│   │   └── socket.ts   # WebSocket setup
│   └── utils/         # Server utilities
│       ├── database/  # Database helpers
│       │   ├── queries.ts
│       │   └── models.ts
│       ├── auth/      # Auth utilities
│       │   ├── jwt.ts
│       │   └── crypto.ts
│       ├── cache/     # Caching utilities
│       │   ├── redis.ts
│       │   └── memory.ts
│       ├── monitoring/ # Server monitoring
│       │   └── metrics.ts
│       ├── security/  # Security utilities
│       │   └── encryption.ts
│       └── validation/ # Data validation
│           └── schemas.ts
│
├── shared/              # Universal code (client+server)
│   └── utils/          # Shared utilities
│       ├── datetime.ts # Date formatting
│       └── validation.ts # Shared validation
│
├── utils/              # Client-side utilities
│   ├── formatting.ts   # Data formatting
│   ├── validation.ts   # Client validation
│   └── helpers.ts      # General helpers
│
├── test/               # Testing files
│   ├── unit/          # Unit tests
│   │   ├── components/
│   │   └── composables/
│   └── e2e/           # End-to-end tests
│       └── specs/
│
├── .env               # Development env vars (git-ignored)
├── .env.example       # Example env vars template
├── .gitignore         # Git ignore patterns
├── app.vue            # Root Vue component
├── app.config.ts      # Runtime config
├── error.vue          # Error page
├── nuxt.config.ts     # Nuxt configuration
├── package.json       # Project dependencies
├── tsconfig.json      # TypeScript config
└── README.md          # Project documentation

Special Notes:
1. File Patterns:
   - *.client.* : Client-only code
   - *.server.* : Server-only code
   - *.global.* : Runs on every route
   - *.island.* : Independently rendered
   - [param]    : Required parameter
   - [[param]]  : Optional parameter
   - [...slug]  : Catch-all pattern

2. Auto-imports:
   - Components: Auto-imported by PascalCase
   - Composables: Must start with 'use'
   - Utils: Auto-imported from utils/
   - Server Utils: Server context only

3. Best Practices:
   - Components need single root element
   - API routes support method chaining
   - Middleware can be async
   - Server plugins support Nitro storage
   - Components support Suspense
   - Environment variables need runtime config