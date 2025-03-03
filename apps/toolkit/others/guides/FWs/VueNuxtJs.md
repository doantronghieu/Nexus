# Comprehensive Vue 3 and Nuxt.js Development Guide

- [Comprehensive Vue 3 and Nuxt.js Development Guide](#comprehensive-vue-3-and-nuxtjs-development-guide)
- [1. Project Initialization and Setup](#1-project-initialization-and-setup)
- [2. Core Development](#2-core-development)
  - [2.1 Components](#21-components)
    - [2.1.1 Single File Components (SFCs)](#211-single-file-components-sfcs)
    - [2.1.2 Component Registration](#212-component-registration)
    - [2.1.3 Component Lifecycle](#213-component-lifecycle)
    - [2.1.4 Data and Reactivity](#214-data-and-reactivity)
    - [2.1.5 Computed Properties](#215-computed-properties)
    - [2.1.6 Methods](#216-methods)
    - [2.1.7 Watchers](#217-watchers)
    - [2.1.8 Props](#218-props)
    - [2.1.9 Events](#219-events)
    - [2.1.10 Slots](#2110-slots)
    - [2.1.11 Provide/Inject](#2111-provideinject)
    - [2.1.12 Composition API](#2112-composition-api)
    - [2.1.13 Composables](#2113-composables)
    - [2.1.14 Teleport](#2114-teleport)
    - [2.1.15 Suspense](#2115-suspense)
    - [2.1.16 Dynamic Components](#2116-dynamic-components)
    - [2.1.17 Render Functions and JSX](#2117-render-functions-and-jsx)
    - [2.1.18 Custom Directives](#2118-custom-directives)
    - [2.1.19 Plugins](#2119-plugins)
    - [2.1.20 Advanced Component Patterns](#2120-advanced-component-patterns)
      - [Renderless Components](#renderless-components)
      - [Higher-Order Components](#higher-order-components)
  - [2.2 Application Structure and Optimization](#22-application-structure-and-optimization)
    - [2.2.1 Vue CLI and Nuxt Project Setup](#221-vue-cli-and-nuxt-project-setup)
    - [2.2.2 Folder Structure Best Practices](#222-folder-structure-best-practices)
    - [2.2.3 Lazy Loading and Code Splitting](#223-lazy-loading-and-code-splitting)
    - [2.2.4 Static Site Generation vs. Server-side Rendering](#224-static-site-generation-vs-server-side-rendering)
    - [2.2.5 Nuxt.js Directory Structure and Special Directories](#225-nuxtjs-directory-structure-and-special-directories)
    - [2.2.6 Nuxt Modules and Plugins](#226-nuxt-modules-and-plugins)
  - [2.3 Routing and Navigation](#23-routing-and-navigation)
    - [2.3.1 Vue Router Basics](#231-vue-router-basics)
    - [2.3.2 Nuxt File-based Routing](#232-nuxt-file-based-routing)
    - [2.3.3 Navigation Guards and Middleware](#233-navigation-guards-and-middleware)
    - [2.3.4 Route Meta Fields](#234-route-meta-fields)
    - [2.3.5 Lazy Loading Routes](#235-lazy-loading-routes)
    - [2.3.6 Nested Routes and Dynamic Route Matching](#236-nested-routes-and-dynamic-route-matching)
    - [2.3.7 Programmatic Navigation](#237-programmatic-navigation)
    - [2.3.8 Handling Navigation Errors](#238-handling-navigation-errors)
    - [2.3.9 Scroll Behavior Management](#239-scroll-behavior-management)
    - [2.3.10 Transitions Between Routes](#2310-transitions-between-routes)
  - [2.4 State Management](#24-state-management)
    - [2.4.1 Component Local State](#241-component-local-state)
    - [2.4.2 Pinia for Global State Management](#242-pinia-for-global-state-management)
    - [2.4.3 When to Use Local vs Global State](#243-when-to-use-local-vs-global-state)
    - [2.4.4 State Management Patterns for Large Applications](#244-state-management-patterns-for-large-applications)
    - [2.4.5 Handling State in SSR Context](#245-handling-state-in-ssr-context)
    - [2.4.6 Persisting and Rehydrating State](#246-persisting-and-rehydrating-state)
    - [2.4.7 DevTools Integration for Debugging](#247-devtools-integration-for-debugging)
  - [2.5 Forms and User Input](#25-forms-and-user-input)
    - [2.5.1 Form Handling in Vue.js](#251-form-handling-in-vuejs)
    - [2.5.2 Custom Form Controls](#252-custom-form-controls)
    - [2.5.3 Form Validation Techniques](#253-form-validation-techniques)
    - [2.5.4 Handling File Uploads](#254-handling-file-uploads)
    - [2.5.5 Implementing Complex Forms (Multi-step, Dynamic Fields)](#255-implementing-complex-forms-multi-step-dynamic-fields)
  - [2.6 API Integration and Data Handling](#26-api-integration-and-data-handling)
    - [2.6.1 Making HTTP Requests (Axios, Fetch API)](#261-making-http-requests-axios-fetch-api)
    - [2.6.2 RESTful API Integration](#262-restful-api-integration)
    - [2.6.3 GraphQL Integration with Apollo](#263-graphql-integration-with-apollo)
    - [2.6.4 Real-time Updates with WebSockets](#264-real-time-updates-with-websockets)
    - [2.6.5 Handling API Errors and Loading States](#265-handling-api-errors-and-loading-states)
    - [2.6.6 Data Fetching in Nuxt (asyncData, fetch)](#266-data-fetching-in-nuxt-asyncdata-fetch)
    - [2.6.7 Caching and State Persistence Strategies](#267-caching-and-state-persistence-strategies)
    - [2.6.8 Authentication (JWT, OAuth)](#268-authentication-jwt-oauth)
    - [2.6.9 Request/Response Interceptors](#269-requestresponse-interceptors)
    - [2.6.10 Rate Limiting and Throttling](#2610-rate-limiting-and-throttling)
    - [2.6.11 Setting up Mock APIs for Development](#2611-setting-up-mock-apis-for-development)
- [3. Styling and UI](#3-styling-and-ui)
  - [3.1 CSS in Vue Components](#31-css-in-vue-components)
    - [3.1.1 Scoped CSS](#311-scoped-css)
    - [3.1.2 CSS Modules](#312-css-modules)
    - [3.1.3 Global Styles](#313-global-styles)
    - [3.1.4 Dynamic Styling](#314-dynamic-styling)
  - [3.2 Preprocessors](#32-preprocessors)
    - [3.2.1 SCSS](#321-scss)
    - [3.2.2 Less](#322-less)
  - [3.3 Tailwind CSS Integration](#33-tailwind-css-integration)
    - [3.3.1 Setup in Nuxt.js](#331-setup-in-nuxtjs)
    - [3.3.2 Using Tailwind Classes](#332-using-tailwind-classes)
    - [3.3.3 Customizing Tailwind](#333-customizing-tailwind)
    - [3.3.4 Responsive Design with Tailwind](#334-responsive-design-with-tailwind)
  - [3.4 CSS Custom Properties (Variables)](#34-css-custom-properties-variables)
    - [3.4.1 Defining and Using CSS Variables](#341-defining-and-using-css-variables)
    - [3.4.2 Dynamic CSS Variables](#342-dynamic-css-variables)
  - [3.5 Advanced UI Patterns](#35-advanced-ui-patterns)
    - [3.5.1 Responsive Layout with CSS Grid](#351-responsive-layout-with-css-grid)
    - [3.5.2 Theming](#352-theming)
    - [3.5.3 CSS Transitions and Animations](#353-css-transitions-and-animations)
  - [3.6 UI Components](#36-ui-components)
    - [3.6.1 Modal Component](#361-modal-component)
    - [3.6.2 Tabs Component](#362-tabs-component)
    - [3.6.3 Infinite Scroll](#363-infinite-scroll)
    - [3.6.4 Data Table Component](#364-data-table-component)
    - [3.6.5 Tree View Component](#365-tree-view-component)
    - [3.6.6 Rich Text Editor](#366-rich-text-editor)
  - [3.7 Accessibility Considerations](#37-accessibility-considerations)
    - [3.7.1 Semantic HTML](#371-semantic-html)
    - [3.7.2 ARIA Attributes](#372-aria-attributes)
    - [3.7.3 Keyboard Navigation](#373-keyboard-navigation)
  - [3.8 Internationalization (i18n) in UI](#38-internationalization-i18n-in-ui)
  - [3.9 Advanced Animation Techniques](#39-advanced-animation-techniques)
    - [3.9.1 Using GSAP (GreenSock Animation Platform)](#391-using-gsap-greensock-animation-platform)
    - [3.9.2 Vue Transition Group for List Animations](#392-vue-transition-group-for-list-animations)
  - [3.10 Responsive Design Patterns](#310-responsive-design-patterns)
    - [3.10.1 Mobile-First Approach](#3101-mobile-first-approach)
    - [3.10.2 Responsive Images](#3102-responsive-images)
  - [3.11 Advanced CSS Techniques](#311-advanced-css-techniques)
    - [3.11.1 CSS Grid for Complex Layouts](#3111-css-grid-for-complex-layouts)
    - [3.11.2 CSS Custom Properties for Theming](#3112-css-custom-properties-for-theming)
  - [3.12 Performance Optimization for UI](#312-performance-optimization-for-ui)
    - [3.12.1 Lazy Loading Components](#3121-lazy-loading-components)
    - [3.12.2 Virtual Scrolling for Large Lists](#3122-virtual-scrolling-for-large-lists)
    - [3.12.3 Debouncing and Throttling](#3123-debouncing-and-throttling)
  - [3.13 Advanced Form Handling](#313-advanced-form-handling)
    - [3.13.1 Form Validation with Vee-Validate](#3131-form-validation-with-vee-validate)
    - [3.13.2 Dynamic Form Fields](#3132-dynamic-form-fields)
  - [3.14 Micro-Interactions and Animations](#314-micro-interactions-and-animations)
    - [3.14.1 Button Click Animation](#3141-button-click-animation)
    - [3.14.2 Hover Effects](#3142-hover-effects)
  - [3.15 Design Systems and Component Libraries](#315-design-systems-and-component-libraries)
    - [3.15.1 Creating a Button Component](#3151-creating-a-button-component)
- [4. Performance Optimization](#4-performance-optimization)
- [5. SEO and Metadata](#5-seo-and-metadata)
- [6. Internationalization (i18n)](#6-internationalization-i18n)
- [7. Testing](#7-testing)
- [8. Security](#8-security)
- [9. Deployment and DevOps](#9-deployment-and-devops)
- [10. Best Practices](#10-best-practices)
  - [10.1 Code Quality and Development](#101-code-quality-and-development)
  - [10.2 Performance Optimization](#102-performance-optimization)
  - [10.3 State Management](#103-state-management)
  - [10.4 Error Handling and Debugging](#104-error-handling-and-debugging)
  - [10.5 Asynchronous Operations](#105-asynchronous-operations)
  - [10.6 Security](#106-security)
  - [10.7 Internationalization and Localization](#107-internationalization-and-localization)
  - [10.8 SEO and Accessibility](#108-seo-and-accessibility)
  - [10.9 Deployment and DevOps](#109-deployment-and-devops)
  - [10.10 Version Control](#1010-version-control)
  - [10.11 UI/UX Best Practices](#1011-uiux-best-practices)
  - [10.12 Memory Management](#1012-memory-management)
  - [10.13 Vue.js Specific Best Practices](#1013-vuejs-specific-best-practices)
  - [10.14 Nuxt.js Specific Optimizations](#1014-nuxtjs-specific-optimizations)
  - [10.15 Testing Best Practices](#1015-testing-best-practices)
  - [10.16 Documentation Best Practices](#1016-documentation-best-practices)
- [11. Ecosystem and Third-Party Integrations](#11-ecosystem-and-third-party-integrations)
- [Conclusion](#conclusion)


# 1. Project Initialization and Setup
- Choose Nuxt 3 for project initialization
  - Use `npx nuxi init project-name` command
- Configure Vue 3 and ensure compatibility
- Set up folder structure:
  - components/
  - pages/
  - layouts/
  - assets/
  - plugins/
  - store/ (for Pinia)
  - composables/
  - utils/
  - types/ (if using TypeScript)
  - middleware/
  - server/ (for server-side logic)
- Configure Nuxt's file-based routing
- Set up Pinia for state management
  - Install with `npm install pinia @pinia/nuxt`
  - Add to `modules` in `nuxt.config.ts`
- Install and configure Tailwind CSS
  - Use `npx nuxi module add @nuxtjs/tailwindcss`
  - Create `tailwind.config.js` and `assets/css/tailwind.css`
- Set up environment variables
  - Create `.env`, `.env.development`, and `.env.production` files
  - Use `runtimeConfig` in `nuxt.config.ts` for exposing variables
- Configure TypeScript (if using)
  - Ensure `tsconfig.json` is properly set up
- Set up linting and formatting:
  - ESLint: `npm install --save-dev eslint @nuxtjs/eslint-config-typescript`
  - Prettier: `npm install --save-dev prettier eslint-plugin-prettier`
  - Stylelint: `npm install --save-dev stylelint stylelint-config-standard`
- Set up testing framework:
  - Vitest: `npm install --save-dev vitest @vue/test-utils`
  - Cypress: `npm install --save-dev cypress`
- Configure build tools and optimization (Vite is default with Nuxt 3)
- Set up version control (Git):
  - Initialize repository: `git init`
  - Create `.gitignore` file (include `.nuxt`, `node_modules`, etc.)
- Configure npm as the package manager
  - Create `.npmrc` for any custom configurations
- Set up editor configuration (.editorconfig)

# 2. Core Development

## 2.1 Components

### 2.1.1 Single File Components (SFCs)

Vue components are typically created using Single File Components (SFCs). An SFC contains the template, script, and style for a component in a single .vue file.

```vue
<template>
  <div class="example">{{ message }}</div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('Hello, Vue 3!')
</script>

<style scoped>
.example {
  color: red;
}
</style>
```

### 2.1.2 Component Registration

Components can be registered globally or locally. With the Composition API, local registration is often preferred:

```vue
<script setup>
import ChildComponent from './ChildComponent.vue'
</script>

<template>
  <ChildComponent />
</template>
```

### 2.1.3 Component Lifecycle

Vue 3 components have several lifecycle hooks:

```vue
<script setup>
import { onMounted, onUpdated, onUnmounted } from 'vue'

onMounted(() => {
  console.log('Component is mounted')
})

onUpdated(() => {
  console.log('Component is updated')
})

onUnmounted(() => {
  console.log('Component is unmounted')
})
</script>
```

### 2.1.4 Data and Reactivity

In the Composition API, we use `ref` and `reactive` for reactivity:

```vue
<script setup>
import { ref, reactive } from 'vue'

const count = ref(0)
const state = reactive({ message: 'Hello' })
</script>
```

### 2.1.5 Computed Properties

Computed properties are created using the `computed` function:

```vue
<script setup>
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
</script>
```

### 2.1.6 Methods

In the Composition API, methods are simply functions declared in the `setup` function:

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
const increment = () => {
  count.value++
}
</script>
```

### 2.1.7 Watchers

Watchers are created using the `watch` or `watchEffect` functions:

```vue
<script setup>
import { ref, watch, watchEffect } from 'vue'

const count = ref(0)

watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
})

watchEffect(() => {
  console.log(`Count is now: ${count.value}`)
})
</script>
```

### 2.1.8 Props

Props are defined using the `defineProps` compiler macro:

```vue
<script setup>
const props = defineProps({
  message: String,
  count: {
    type: Number,
    required: true,
    default: 0
  }
})
</script>
```

### 2.1.9 Events

Events are emitted using the `defineEmits` compiler macro:

```vue
<script setup>
const emit = defineEmits(['update', 'delete'])

const updateItem = () => {
  emit('update', { id: 1, name: 'Updated Item' })
}
</script>
```

### 2.1.10 Slots

Slots allow content distribution from parent to child components:

```vue
<!-- Parent component -->
<template>
  <ChildComponent>
    <template #header>
      <h1>Header Content</h1>
    </template>
    <template #default>
      <p>Default Content</p>
    </template>
    <template #footer>
      <p>Footer Content</p>
    </template>
  </ChildComponent>
</template>

<!-- Child component -->
<template>
  <div>
    <slot name="header"></slot>
    <slot></slot>
    <slot name="footer"></slot>
  </div>
</template>
```

### 2.1.11 Provide/Inject

Provide/Inject allows passing data deeply through the component tree:

```vue
<!-- Parent component -->
<script setup>
import { provide, ref } from 'vue'

const theme = ref('light')
provide('theme', theme)
</script>

<!-- Descendant component -->
<script setup>
import { inject } from 'vue'

const theme = inject('theme', 'light') // 'light' is the default value
</script>
```

### 2.1.12 Composition API

The Composition API provides a more flexible way to organize component logic:

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

const increment = () => {
  count.value++
}

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double Count: {{ doubleCount }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

### 2.1.13 Composables

Composables are reusable pieces of logic that can be shared between components:

```javascript
// useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  return {
    count,
    doubleCount,
    increment
  }
}

// Component using the composable
<script setup>
import { useCounter } from './useCounter'

const { count, doubleCount, increment } = useCounter()
</script>
```

### 2.1.14 Teleport

Teleport allows rendering content at a different place in the DOM tree:

```vue
<template>
  <div>
    <teleport to="body">
      <div class="modal">
        <!-- Modal content -->
      </div>
    </teleport>
  </div>
</template>
```

### 2.1.15 Suspense

Suspense provides a way to handle asynchronous dependencies in the template:

```vue
<template>
  <Suspense>
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() => import('./AsyncComponent.vue'))
</script>
```

### 2.1.16 Dynamic Components

Dynamic components allow switching between multiple components:

```vue
<template>
  <component :is="currentComponent"></component>
</template>

<script setup>
import { ref, shallowRef } from 'vue'
import ComponentA from './ComponentA.vue'
import ComponentB from './ComponentB.vue'

const currentComponent = shallowRef(ComponentA)

const switchComponent = () => {
  currentComponent.value = currentComponent.value === ComponentA ? ComponentB : ComponentA
}
</script>
```

### 2.1.17 Render Functions and JSX

For complex template logic, render functions and JSX can be used:

```vue
<script setup>
import { h } from 'vue'

const render = () => {
  return h('div', {}, [
    h('h1', {}, 'Title'),
    h('p', {}, 'Content')
  ])
}
</script>

<template>
  <render />
</template>
```

With JSX (requires proper Babel setup):

```vue
<script setup>
const render = () => {
  return (
    <div>
      <h1>Title</h1>
      <p>Content</p>
    </div>
  )
}
</script>

<template>
  <render />
</template>
```

### 2.1.18 Custom Directives

Custom directives allow low-level DOM access on elements:

```vue
<script setup>
import { directive } from 'vue'

const vFocus = {
  mounted: (el) => el.focus()
}

directive('focus', vFocus)
</script>

<template>
  <input v-focus />
</template>
```

### 2.1.19 Plugins

Plugins allow adding global-level functionality to Vue:

```javascript
// plugin.js
export default {
  install: (app, options) => {
    app.config.globalProperties.$myMethod = () => {
      // some logic
    }
  }
}

// main.js
import { createApp } from 'vue'
import App from './App.vue'
import myPlugin from './plugin'

const app = createApp(App)
app.use(myPlugin)
app.mount('#app')
```

### 2.1.20 Advanced Component Patterns

#### Renderless Components

Renderless components manage logic but delegate rendering to the parent:

```vue
<!-- RenderlessCounter.vue -->
<script setup>
import { ref } from 'vue'

const count = ref(0)
const increment = () => count.value++

defineExpose({ count, increment })
</script>

<template>
  <slot :count="count" :increment="increment" />
</template>

<!-- Usage -->
<template>
  <RenderlessCounter v-slot="{ count, increment }">
    <div>
      Count: {{ count }}
      <button @click="increment">Increment</button>
    </div>
  </RenderlessCounter>
</template>
```

#### Higher-Order Components

Higher-Order Components (HOCs) are functions that take a component and return a new component with added functionality:

```javascript
// withLogging.js
export function withLogging(WrappedComponent) {
  return {
    setup(props, { attrs, slots }) {
      console.log('Component rendered with props:', props)
      return () => h(WrappedComponent, attrs, slots)
    }
  }
}

// Usage
import { withLogging } from './withLogging'
import BaseComponent from './BaseComponent.vue'

const EnhancedComponent = withLogging(BaseComponent)
```

## 2.2 Application Structure and Optimization

### 2.2.1 Vue CLI and Nuxt Project Setup

For Vue CLI:
```bash
npm install -g @vue/cli
vue create my-project
cd my-project
npm run serve
```

For Nuxt:
```bash
npx create-nuxt-app my-nuxt-project
cd my-nuxt-project
npm run dev
```

### 2.2.2 Folder Structure Best Practices

```
src/
  assets/
  components/
  composables/
  layouts/ (Nuxt)
  pages/ (Nuxt)
  plugins/
  router/
  store/
  utils/
```

### 2.2.3 Lazy Loading and Code Splitting

```vue
<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() => import('./HeavyComponent.vue'))
</script>

<template>
  <AsyncComponent />
</template>
```

### 2.2.4 Static Site Generation vs. Server-side Rendering

For Nuxt, configure in `nuxt.config.js`:

```javascript
export default {
  // SSR
  ssr: true,

  // Static Site Generation
  target: 'static'
}
```

### 2.2.5 Nuxt.js Directory Structure and Special Directories

Nuxt automatically configures routing based on the `pages/` directory structure.

### 2.2.6 Nuxt Modules and Plugins

```javascript
// nuxt.config.js
export default {
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/pwa'
  ],
  plugins: [
    '~/plugins/my-plugin.js'
  ]
}
```

## 2.3 Routing and Navigation

### 2.3.1 Vue Router Basics

```vue
<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navigateTo = () => {
  router.push('/new-page')
}
</script>
```

### 2.3.2 Nuxt File-based Routing

Create files in the `pages/` directory, and Nuxt will automatically generate routes.

### 2.3.3 Navigation Guards and Middleware

```javascript
// Router navigation guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

// Nuxt middleware
export default function ({ store, redirect }) {
  if (!store.state.isAuthenticated) {
    return redirect('/login')
  }
}
```

### 2.3.4 Route Meta Fields

```javascript
const routes = [
  {
    path: '/admin',
    component: Admin,
    meta: { requiresAuth: true }
  }
]
```

### 2.3.5 Lazy Loading Routes

```javascript
const routes = [
  {
    path: '/user/:id',
    component: () => import('./views/User.vue')
  }
]
```

### 2.3.6 Nested Routes and Dynamic Route Matching

```vue
<!-- Parent component -->
<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<!-- Route configuration -->
<script setup>
const routes = [
  {
    path: '/user/:id',
    component: User,
    children: [
      {
        path: 'profile',
        component: UserProfile
      },
      {
        path: 'posts',
        component: UserPosts
      }
    ]
  }
]
</script>
```

### 2.3.7 Programmatic Navigation

```vue
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>
```

### 2.3.8 Handling Navigation Errors

```vue
<script setup>
import { onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onErrorCaptured((err, instance, info) => {
  router.push('/error')
  return false // Prevent error from propagating further
})
</script>
```

### 2.3.9 Scroll Behavior Management

```javascript
const router = createRouter({
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})
```

### 2.3.10 Transitions Between Routes

```vue
<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

## 2.4 State Management

### 2.4.1 Component Local State

```vue
<script setup>
import { ref, reactive } from 'vue'

const count = ref(0)
const user = reactive({
  name: 'John Doe',
  age: 30
})
</script>
```

### 2.4.2 Pinia for Global State Management

```javascript
// store/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
})

// Component usage
<script setup>
import { useCounterStore } from '@/store/counter'

const counter = useCounterStore()
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double Count: {{ counter.doubleCount }}</p>
    <button @click="counter.increment">Increment</button>
  </div>
</template>
```

### 2.4.3 When to Use Local vs Global State

- Use local state for component-specific data that doesn't need to be shared.
- Use global state (Pinia) for data that needs to be accessed by multiple components or persisted across route changes.

### 2.4.4 State Management Patterns for Large Applications

- Module-based store structure
- Namespaced modules
- Action composition

```javascript
// store/index.js
import { createPinia } from 'pinia'
import { useUserStore } from './user'
import { useProductStore } from './product'

const pinia = createPinia()

export { pinia, useUserStore, useProductStore }

// store/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  // state, getters, actions
})

// store/product.js
import { defineStore } from 'pinia'

export const useProductStore = defineStore('product', {
  // state, getters, actions
})
```

### 2.4.5 Handling State in SSR Context

For Nuxt with Pinia:

```javascript
// nuxt.config.js
export default {
  buildModules: [
    '@pinia/nuxt',
  ],
}

// store/index.js
import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    counter: 0,
  }),
  actions: {
    increment() {
      this.counter++
    },
  },
})

// Component usage in Nuxt
<script setup>
import { useMainStore } from '@/store'

const mainStore = useMainStore()
</script>
```

### 2.4.6 Persisting and Rehydrating State

```javascript
// store/index.js
import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(createPersistedState({
  storage: localStorage,
  key: prefix => `${prefix}`,
}))

export default pinia
```

### 2.4.7 DevTools Integration for Debugging

Pinia integrates automatically with Vue DevTools, providing a great debugging experience.

## 2.5 Forms and User Input

### 2.5.1 Form Handling in Vue.js

```vue
<template>
  <form @submit.prevent="submitForm">
    <input v-model="form.name" type="text" />
    <input v-model="form.email" type="email" />
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  email: ''
})

const submitForm = () => {
  // Handle form submission
  console.log(form)
}
</script>
```

### 2.5.2 Custom Form Controls

```vue
<template>
  <label>
    {{ label }}
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      v-bind="$attrs"
    >
  </label>
</template>

<script setup>
defineProps(['label', 'modelValue'])
defineEmits(['update:modelValue'])
</script>
```

### 2.5.3 Form Validation Techniques

Using vee-validate:

```vue
<template>
  <Form @submit="onSubmit">
    <Field name="email" v-slot="{ field, errors }">
      <input v-bind="field" type="email">
      <span>{{ errors[0] }}</span>
    </Field>
    <button>Submit</button>
  </Form>
</template>

<script setup>
import { Form, Field } from 'vee-validate'
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().required().email(),
})

const onSubmit = values => {
  console.log(values)
}
</script>
```

### 2.5.4 Handling File Uploads

```vue
<template>
  <input type="file" @change="handleFileUpload">
</template>

<script setup>
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  const formData = new FormData()
  formData.append('file', file)
  
  // Send formData to server
}
</script>
```

### 2.5.5 Implementing Complex Forms (Multi-step, Dynamic Fields)

```vue
<template>
  <form @submit.prevent="submitForm">
    <template v-if="step === 1">
      <!-- Step 1 fields -->
    </template>
    <template v-else-if="step === 2">
      <!-- Step 2 fields -->
    </template>
    <template v-else>
      <!-- Step 3 fields -->
    </template>
    
    <button v-if="step > 1" @click="prevStep">Previous</button>
    <button v-if="step < 3" @click="nextStep">Next</button>
    <button v-else type="submit">Submit</button>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const step = ref(1)
const form = reactive({
  // form fields
})

const nextStep = () => {
  if (step.value < 3) step.value++
}

const prevStep = () => {
  if (step.value > 1) step.value--
}

const submitForm = () => {
  // Handle form submission
}
</script>
```

## 2.6 API Integration and Data Handling

### 2.6.1 Making HTTP Requests (Axios, Fetch API)

Using Axios:

```javascript
import axios from 'axios'

const fetchData = async () => {
  try {
    const response = await axios.get('https://api.example.com/data')
    console.log(response.data)
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}
```

### 2.6.2 RESTful API Integration

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.example.com',
})

export const getUserData = (userId) => api.get(`/users/${userId}`)
export const updateUserData = (userId, data) => api.put(`/users/${userId}`, data)
export const createUser = (data) => api.post('/users', data)
export const deleteUser = (userId) => api.delete(`/users/${userId}`)
```

### 2.6.3 GraphQL Integration with Apollo

```vue
<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <ul v-else>
    <li v-for="user in users" :key="user.id">{{ user.name }}</li>
  </ul>
</template>

<script setup>
import { useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'

const USERS_QUERY = gql`
  query GetUsers {
    users {
      id
      name
    }
  }
`

const { result, loading, error } = useQuery(USERS_QUERY)
const users = computed(() => result.value?.users ?? [])
</script>
```

### 2.6.4 Real-time Updates with WebSockets

```javascript
import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket(url) {
  const data = ref(null)
  const error = ref(null)
  let socket

  onMounted(() => {
    socket = new WebSocket(url)
    
    socket.onmessage = (event) => {
      data.value = JSON.parse(event.data)
    }
    
    socket.onerror = (event) => {
      error.value = event
    }
  })

  onUnmounted(() => {
    if (socket) {
      socket.close()
    }
  })

  return { data, error }
}

// Usage in a component
const { data, error } = useWebSocket('wss://example.com/socket')
```

### 2.6.5 Handling API Errors and Loading States

```vue
<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <div v-else>
    {{ data }}
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const data = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('https://api.example.com/data')
    data.value = response.data
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}

fetchData()
</script>
```

### 2.6.6 Data Fetching in Nuxt (asyncData, fetch)

```vue
<script setup>
const { data } = await useFetch('/api/users')
</script>

<template>
  <div>
    <h1>Users</h1>
    <ul>
      <li v-for="user in data" :key="user.id">{{ user.name }}</li>
    </ul>
  </div>
</template>
```

### 2.6.7 Caching and State Persistence Strategies

Using Pinia with persistedstate:

```javascript
import { defineStore } from 'pinia'
import { persistedState } from 'pinia-plugin-persistedstate'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
  }),
  actions: {
    setUser(user) {
      this.user = user
    },
  },
  persist: true,
})
```

### 2.6.8 Authentication (JWT, OAuth)

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.example.com',
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export const login = async (credentials) => {
  const response = await api.post('/login', credentials)
  localStorage.setItem('token', response.data.token)
  return response.data
}

export const logout = () => {
  localStorage.removeItem('token')
}
```

### 2.6.9 Request/Response Interceptors

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://api.example.com',
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Modify request config
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      // Handle unauthorized error
    }
    return Promise.reject(error)
  }
)
```

### 2.6.10 Rate Limiting and Throttling

```javascript
import axios from 'axios'
import rateLimit from 'axios-rate-limit'

const api = rateLimit(
  axios.create({
    baseURL: 'https://api.example.com',
  }),
  { maxRequests: 2, perMilliseconds: 1000 }
)
```

### 2.6.11 Setting up Mock APIs for Development

Using Mirage JS:

```javascript
import { createServer, Model } from 'miragejs'

export function makeServer({ environment = 'development' } = {}) {
  let server = createServer({
    environment,

    models: {
      user: Model,
    },

    seeds(server) {
      server.create('user', { name: 'Bob' })
      server.create('user', { name: 'Alice' })
    },

    routes() {
      this.namespace = 'api'

      this.get('/users', (schema) => {
        return schema.users.all()
      })
    },
  })

  return server
}

// In main.js
if (process.env.NODE_ENV === 'development') {
  makeServer()
}
```

This completes the expanded Section 2 on Core Development. Next, I'll provide the updated Section 3 on Styling and UI.

# 3. Styling and UI

## 3.1 CSS in Vue Components

### 3.1.1 Scoped CSS

```vue
<template>
  <div class="example">Scoped CSS Example</div>
</template>

<style scoped>
.example {
  color: red;
}
</style>
```

### 3.1.2 CSS Modules

```vue
<template>
  <div :class="$style.example">CSS Modules Example</div>
</template>

<style module>
.example {
  color: blue;
}
</style>
```

### 3.1.3 Global Styles

```javascript
// main.js or nuxt.config.js
import './assets/global.css'
```

### 3.1.4 Dynamic Styling

```vue
<template>
  <div :style="{ color: dynamicColor, fontSize: fontSize + 'px' }">
    Dynamic Styling
  </div>
</template>

<script setup>
import { ref } from 'vue'

const dynamicColor = ref('red')
const fontSize = ref(16)
</script>
```

## 3.2 Preprocessors

### 3.2.1 SCSS

```vue
<style lang="scss">
$primary-color: #3490dc;

.button {
  background-color: $primary-color;
  &:hover {
    background-color: darken($primary-color, 10%);
  }
}
</style>
```

### 3.2.2 Less

```vue
<style lang="less">
@primary-color: #3490dc;

.button {
  background-color: @primary-color;
  &:hover {
    background-color: darken(@primary-color, 10%);
  }
}
</style>
```

## 3.3 Tailwind CSS Integration

### 3.3.1 Setup in Nuxt.js

```bash
npm install -D @nuxtjs/tailwindcss tailwindcss@latest postcss@latest autoprefixer@latest
```

```javascript
// nuxt.config.js
export default {
  buildModules: ['@nuxtjs/tailwindcss']
}
```

### 3.3.2 Using Tailwind Classes

```vue
<template>
  <div class="bg-gray-200 p-4 rounded-lg shadow-md">
    <h1 class="text-2xl font-bold text-blue-600">Hello, Tailwind!</h1>
  </div>
</template>
```

### 3.3.3 Customizing Tailwind

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'custom-blue': '#3490dc',
      },
    },
  },
  variants: {},
  plugins: [],
}
```

### 3.3.4 Responsive Design with Tailwind

```vue
<template>
  <div class="text-sm sm:text-base md:text-lg lg:text-xl">
    Responsive Text
  </div>
</template>
```

## 3.4 CSS Custom Properties (Variables)

### 3.4.1 Defining and Using CSS Variables

```vue
<template>
  <div class="example">CSS Variables Example</div>
</template>

<style>
:root {
  --primary-color: #3490dc;
}

.example {
  color: var(--primary-color);
}
</style>
```

### 3.4.2 Dynamic CSS Variables

```vue
<template>
  <div class="example" :style="{ '--dynamic-color': color }">
    Dynamic CSS Variable
  </div>
</template>

<script setup>
import { ref } from 'vue'

const color = ref('#3490dc')
</script>

<style>
.example {
  color: var(--dynamic-color);
}
</style>
```

## 3.5 Advanced UI Patterns

### 3.5.1 Responsive Layout with CSS Grid

```vue
<template>
  <div class="grid-container">
    <div class="header">Header</div>
    <div class="sidebar">Sidebar</div>
    <div class="content">Content</div>
    <div class="footer">Footer</div>
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar content"
    "footer footer";
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.footer { grid-area: footer; }

@media (max-width: 768px) {
  .grid-container {
    grid-template-areas:
      "header"
      "content"
      "sidebar"
      "footer";
    grid-template-columns: 1fr;
  }
}
</style>
```

### 3.5.2 Theming

```vue
<template>
  <div :class="['app', theme]">
    <button @click="toggleTheme">Toggle Theme</button>
    <p>Themed Content</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const theme = ref('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}
</script>

<style scoped>
.app {
  transition: background-color 0.3s, color 0.3s;
}

.light {
  background-color: #ffffff;
  color: #333333;
}

.dark {
  background-color: #333333;
  color: #ffffff;
}
</style>
```

### 3.5.3 CSS Transitions and Animations

```vue
<template>
  <div>
    <button @click="show = !show">Toggle</button>
    <transition name="fade">
      <p v-if="show">Fade me in and out</p>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const show = ref(true)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
```

## 3.6 UI Components

### 3.6.1 Modal Component

```vue
<template>
  <teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click="close">
      <div class="modal" @click.stop>
        <slot></slot>
        <button @click="close">Close</button>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps(['isOpen'])
const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
}
</style>
```

### 3.6.2 Tabs Component

```vue
<template>
  <div class="tabs">
    <div class="tab-headers">
      <button 
        v-for="(tab, index) in tabs" 
        :key="index"
        @click="activeTab = index"
        :class="{ active: activeTab === index }"
      >
        {{ tab.title }}
      </button>
    </div>
    <div class="tab-content">
      <component :is="tabs[activeTab].content" />
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'

const props = defineProps(['tabs'])
const activeTab = ref(0)
</script>

<style scoped>
.tabs {
  /* Tab styles */
}

.tab-headers button.active {
  /* Active tab styles */
}

.tab-content {
  /* Tab content styles */
}
</style>
```

### 3.6.3 Infinite Scroll

```vue
<template>
  <div class="infinite-scroll" @scroll="handleScroll">
    <div v-for="item in items" :key="item.id">
      {{ item.content }}
    </div>
    <div v-if="loading">Loading...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])
const loading = ref(false)
const page = ref(1)

const loadMore = async () => {
  loading.value = true
  // Fetch more items and add to items array
  loading.value = false
  page.value++
}

const handleScroll = (e) => {
  const { scrollTop, scrollHeight, clientHeight } = e.target
  if (scrollTop + clientHeight >= scrollHeight - 5 && !loading.value) {
    loadMore()
  }
}

onMounted(() => {
  loadMore()
})
</script>

<style scoped>
.infinite-scroll {
  height: 400px;
  overflow-y: auto;
}
</style>
```

### 3.6.4 Data Table Component

```vue
<template>
  <table>
    <thead>
      <tr>
        <th v-for="column in columns" :key="column.key">
          {{ column.label }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in data" :key="row.id">
        <td v-for="column in columns" :key="column.key">
          {{ row[column.key] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({
  columns: Array,
  data: Array
})
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
</style>
```

### 3.6.5 Tree View Component

```vue
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.label }}
      <tree-view v-if="item.children" :items="item.children" />
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: Array
})
</script>
```

### 3.6.6 Rich Text Editor

Using a library like Quill.js:

```vue
<template>
  <div ref="editor"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'

const editor = ref(null)

onMounted(() => {
  new Quill(editor.value, {
    theme: 'snow'
  })
})
</script>
```

## 3.7 Accessibility Considerations

### 3.7.1 Semantic HTML

```vue
<template>
  <header>
    <h1>Page Title</h1>
    <nav>
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <article>
      <h2>Article Title</h2>
      <p>Article content...</p>
    </article>
  </main>
  <footer>
    <p>&copy; 2023 Your Company</p>
  </footer>
</template>
```

### 3.7.2 ARIA Attributes

```vue
<template>
  <div role="tablist">
    <button 
      v-for="(tab, index) in tabs" 
      :key="index"
      role="tab"
      :aria-selected="activeTab === index"
      :aria-controls="`panel-${index}`"
      @click="activeTab = index"
    >
      {{ tab.title }}
    </button>
  </div>
  <div 
    v-for="(tab, index) in tabs" 
    :key="index"
    :id="`panel-${index}`"
    role="tabpanel"
    :aria-labelledby="`tab-${index}`"
    v-show="activeTab === index"
  >
    {{ tab.content }}
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tabs = ref([
  { title: 'Tab 1', content: 'Content 1' },
  { title: 'Tab 2', content: 'Content 2' },
])
const activeTab = ref(0)
</script>
```

### 3.7.3 Keyboard Navigation

```vue
<template>
  <div @keydown.left="previousTab" @keydown.right="nextTab">
    <!-- Tab content -->
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref(0)
const totalTabs = 3

const previousTab = () => {
  activeTab.value = (activeTab.value - 1 + totalTabs) % totalTabs
}

const nextTab = () => {
  activeTab.value = (activeTab.value + 1) % totalTabs
}
</script>
```

## 3.8 Internationalization (i18n) in UI

Using vue-i18n for internationalization:

```vue
<template>
  <div>
    <h1>{{ $t('welcome') }}</h1>
    <p>{{ $t('intro', { name: 'Vue' }) }}</p>
    <button @click="toggleLanguage">
      {{ $t('changeLanguage') }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const toggleLanguage = () => {
  locale.value = locale.value === 'en' ? 'fr' : 'en'
}
</script>
```

```javascript
// i18n.js
import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    welcome: 'Welcome',
    intro: 'Hello, {name}!',
    changeLanguage: 'Change Language'
  },
  fr: {
    welcome: 'Bienvenue',
    intro: 'Bonjour, {name}!',
    changeLanguage: 'Changer de Langue'
  }
}

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages,
})

export default i18n
```

## 3.9 Advanced Animation Techniques

### 3.9.1 Using GSAP (GreenSock Animation Platform)

```vue
<template>
  <div ref="box" class="box"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'

const box = ref(null)

onMounted(() => {
  gsap.to(box.value, {
    duration: 2,
    x: 100,
    rotation: 360,
    ease: 'bounce'
  })
})
</script>

<style scoped>
.box {
  width: 50px;
  height: 50px;
  background-color: #3490dc;
}
</style>
```

### 3.9.2 Vue Transition Group for List Animations

```vue
<template>
  <button @click="shuffle">Shuffle</button>
  <transition-group name="list" tag="ul">
    <li v-for="item in items" :key="item">
      {{ item }}
    </li>
  </transition-group>
</template>

<script setup>
import { ref } from 'vue'

const items = ref([1, 2, 3, 4, 5])

const shuffle = () => {
  items.value = items.value.sort(() => Math.random() - 0.5)
}
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
```

## 3.10 Responsive Design Patterns

### 3.10.1 Mobile-First Approach

```vue
<template>
  <div class="container">
    <div class="content">
      <!-- Content here -->
    </div>
    <aside class="sidebar">
      <!-- Sidebar content -->
    </aside>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}

.content {
  order: 1;
}

.sidebar {
  order: 2;
}

@media (min-width: 768px) {
  .container {
    flex-direction: row;
  }

  .content {
    flex: 1;
    order: 2;
  }

  .sidebar {
    width: 300px;
    order: 1;
  }
}
</style>
```

### 3.10.2 Responsive Images

```vue
<template>
  <picture>
    <source media="(min-width: 650px)" srcset="img-large.jpg">
    <source media="(min-width: 465px)" srcset="img-medium.jpg">
    <img src="img-small.jpg" alt="Description" style="width:auto;">
  </picture>
</template>
```

## 3.11 Advanced CSS Techniques

### 3.11.1 CSS Grid for Complex Layouts

```vue
<template>
  <div class="grid-container">
    <header class="header">Header</header>
    <nav class="nav">Navigation</nav>
    <main class="main">Main Content</main>
    <aside class="sidebar">Sidebar</aside>
    <footer class="footer">Footer</footer>
  </div>
</template>

<style scoped>
.grid-container {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav main sidebar"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  gap: 10px;
  height: 100vh;
}

.header { grid-area: header; }
.nav { grid-area: nav; }
.main { grid-area: main; }
.sidebar { grid-area: sidebar; }
.footer { grid-area: footer; }

@media (max-width: 768px) {
  .grid-container {
    grid-template-areas:
      "header"
      "nav"
      "main"
      "sidebar"
      "footer";
    grid-template-columns: 1fr;
  }
}
</style>
```

### 3.11.2 CSS Custom Properties for Theming

```vue
<template>
  <div class="theme-container">
    <h1>Themed Heading</h1>
    <p>Themed paragraph</p>
    <button @click="toggleTheme">Toggle Theme</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const theme = ref('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.body.setAttribute('data-theme', theme.value)
}
</script>

<style>
:root {
  --bg-color: white;
  --text-color: black;
}

[data-theme="dark"] {
  --bg-color: #333;
  --text-color: white;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
}
</style>
```

## 3.12 Performance Optimization for UI

### 3.12.1 Lazy Loading Components

```vue
<script setup>
import { defineAsyncComponent } from 'vue'

const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
)
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyComponent />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>
```

### 3.12.2 Virtual Scrolling for Large Lists

Using vue-virtual-scroller:

```vue
<template>
  <RecycleScroller
    class="scroller"
    :items="listItems"
    :item-size="32"
  >
    <template #default="{ item }">
      <div class="user">
        {{ item.name }}
      </div>
    </template>
  </RecycleScroller>
</template>

<script setup>
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

const listItems = ref([
  // ... large array of items
])
</script>

<style scoped>
.scroller {
  height: 100vh;
}

.user {
  height: 32px;
  padding: 0 12px;
  display: flex;
  align-items: center;
}
</style>
```

### 3.12.3 Debouncing and Throttling

```vue
<template>
  <input @input="debouncedSearch" />
</template>

<script setup>
import { ref } from 'vue'
import debounce from 'lodash/debounce'

const searchTerm = ref('')

const search = () => {
  // Perform search operation
  console.log('Searching for:', searchTerm.value)
}

const debouncedSearch = debounce((e) => {
  searchTerm.value = e.target.value
  search()
}, 300)
</script>
```

## 3.13 Advanced Form Handling

### 3.13.1 Form Validation with Vee-Validate

```vue
<template>
  <Form @submit="onSubmit">
    <Field name="email" v-slot="{ field, errors }">
      <input v-bind="field" type="email">
      <span>{{ errors[0] }}</span>
    </Field>
    <Field name="password" v-slot="{ field, errors }">
      <input v-bind="field" type="password">
      <span>{{ errors[0] }}</span>
    </Field>
    <button>Submit</button>
  </Form>
</template>

<script setup>
import { Form, Field } from 'vee-validate'
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().required().email(),
  password: yup.string().required().min(8),
})

const onSubmit = values => {
  console.log(values)
}
</script>
```

### 3.13.2 Dynamic Form Fields

```vue
<template>
  <form @submit.prevent="submitForm">
    <div v-for="(field, index) in formFields" :key="index">
      <label :for="field.name">{{ field.label }}</label>
      <input
        :id="field.name"
        v-model="formData[field.name]"
        :type="field.type"
        :required="field.required"
      >
    </div>
    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const formFields = ref([
  { name: 'name', label: 'Name', type: 'text', required: true },
  { name: 'email', label: 'Email', type: 'email', required: true },
  { name: 'age', label: 'Age', type: 'number', required: false },
])

const formData = reactive({})

const submitForm = () => {
  console.log(formData)
}
</script>
```

## 3.14 Micro-Interactions and Animations

### 3.14.1 Button Click Animation

```vue
<template>
  <button @click="animate" ref="button">
    Click Me
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'

const button = ref(null)

const animate = () => {
  gsap.to(button.value, {
    scale: 1.2,
    duration: 0.1,
    yoyo: true,
    repeat: 1
  })
}
</script>
```

### 3.14.2 Hover Effects

```vue
<template>
  <div class="hover-effect">
    Hover Me
  </div>
</template>

<style scoped>
.hover-effect {
  transition: all 0.3s ease;
}

.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
</style>
```

## 3.15 Design Systems and Component Libraries

### 3.15.1 Creating a Button Component

```vue
<template>
  <button
    :class="[
      'btn',
      `btn-${size}`,
      `btn-${variant}`,
      { 'btn-block': block }
    ]"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  block: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.btn {
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-sm { padding: 5px 10px; font-size: 12px; }
.btn-md { padding: 10px 20px; font-size: 14px; }
.btn-lg { padding: 15px 30px; font-size: 16px; }

.btn-primary { background-color: #007bff; color: white; }
.btn-secondary { background-color: #6c757d; color: white; }
.btn-danger { background-color: #dc3545; color: white; }

.btn-block { display: block; width: 100%; }
</style>
```

This comprehensive guide covers the major aspects of styling and UI in Vue 3 and Nuxt.js, including CSS methodologies, preprocessors, Tailwind CSS integration, advanced UI patterns, component creation, accessibility, internationalization, animations, responsive design, performance optimization, and more. It provides syntax examples and use cases for each topic, focusing on the Composition API where applicable.

# 4. Performance Optimization
- Lazy loading (components and routes)
- Image and asset optimization
- Keep-alive for frequently toggled components
- Virtual scrolling for long lists
- Optimize third-party library imports
- SSR and SSG for improved initial load times
- Implement proper caching strategies
- Production builds with minification and tree-shaking
- Code splitting
- HTTP/2 for improved loading performance
- Optimize component re-rendering
- Lazy hydration
- Resource hints (preload, prefetch, preconnect)
- Optimize Vue reactivity system usage
- Monitor and optimize Core Web Vitals (LCP, FID, CLS)

# 5. SEO and Metadata
- Use Nuxt's `useHead` composable for dynamic metadata
- Implement Open Graph tags
- Configure robots.txt and sitemap
- Implement structured data and rich snippets
- Use canonical URLs
- Implement proper heading structure
- Handle dynamic routes for SEO
- Implement proper redirects
- Use hreflang for multilingual sites

# 6. Internationalization (i18n)
- Set up nuxt-i18n module
- Implement language switching
- Use lazy loading for language files
- Handle pluralization and date/number formatting
- Implement RTL support if needed
- Handle SEO for multilingual sites
- Implement locale-specific routing

# 7. Testing
- Unit tests for components and stores
- Integration tests
- End-to-end testing setup
- Use Vue Test Utils
- Implement continuous integration (CI)
- Write snapshot tests
- Implement mocking for API calls
- Use code coverage tools
- Implement performance testing
- Conduct accessibility testing

# 8. Security
- Implement authentication and authorization
- Use HTTPS
- Sanitize user inputs
- Implement CSRF protection
- Use Content Security Policy (CSP)
- Keep dependencies updated
- Implement proper error handling
- Use secure HTTP headers
- Implement rate limiting
- Use secure session management
- Implement proper password hashing
- Configure CORS policies
- Implement secure file upload handling

# 9. Deployment and DevOps
- Set up build process
- Implement continuous deployment (CD)
- Configure SSR with Nuxt
- Consider static site generation
- Set up error logging and monitoring
- Implement caching strategies
- Use a CDN for static assets
- Implement blue-green or canary deployments
- Set up backup and disaster recovery
- Implement health checks and auto-scaling
- Use containerization (Docker)
- Set up staging and production environments
- Implement feature flags
- Use infrastructure as code
- Manage secrets securely

# 10. Best Practices

## 10.1 Code Quality and Development
- Follow Vue 3 and Nuxt 3 style guides
- Implement code reviews and pair programming
- Use proper naming conventions
- Follow SOLID principles
- Use ESLint and Prettier for code consistency
- Use meaningful commit messages
- Implement proper git workflow (e.g., GitFlow)
- Use semantic versioning for your project
- Use TypeScript for improved type safety (optional)

## 10.2 Performance Optimization
- Optimize Tailwind CSS usage
- Use computed properties for derived state
- Implement debounce and throttle where necessary
- Use lazy evaluation and memoization for expensive computations
- Use code splitting and lazy loading effectively
- Optimize component re-rendering
- Use functional components for stateless rendering
- Use shallowRef and shallowReactive when deep reactivity is not needed
- Use Web Workers for CPU-intensive tasks when appropriate
- Implement proper lazy loading techniques for images and other media
- Use proper techniques for optimizing large lists and tables

## 10.3 State Management
- Implement proper state management patterns
- Implement effective state management across components and routes
- Implement proper state persistence techniques when necessary

## 10.4 Error Handling and Debugging
- Implement proper error boundaries
- Utilize Vue DevTools for debugging
- Implement proper error handling and user feedback
- Use proper error tracking and reporting in production
- Implement effective error boundaries and fallback UI

## 10.5 Asynchronous Operations
- Use async/await for asynchronous code
- Implement proper WebSocket handling and connection management
- Use proper strategies for handling and caching API responses

## 10.6 Security
- Follow the principle of least privilege
- Use proper security measures (XSS prevention, CSRF protection, etc.)

## 10.7 Internationalization and Localization
- Implement proper internationalization and localization strategies

## 10.8 SEO and Accessibility
- Use proper SEO techniques for single-page applications
- Implement proper keyboard accessibility

## 10.9 Deployment and DevOps
- Use environment variables for configuration
- Implement proper logging in production
- Use proper deployment and CI/CD practices
- Implement proper performance monitoring and optimization

## 10.10 Version Control
- Use proper version control practices

## 10.11 UI/UX Best Practices
- Implement progressive enhancement
- Use feature detection instead of browser detection
- Implement proper form validation
- Implement effective strategies for handling form state and validation
- Use proper techniques for managing and updating application-wide themes

## 10.12 Memory Management
- Implement proper memory management (clean up event listeners, timers)

## 10.13 Vue.js Specific Best Practices
- Implement proper prop validation
- Use key attributes effectively in v-for loops
- Avoid using v-if with v-for on the same element

## 10.14 Nuxt.js Specific Optimizations
- Utilize Nuxt modules effectively
- Use Nuxt's built-in components (e.g., `<NuxtLink>`)
- Implement layouts for consistent page structures
- Use Nuxt's image optimization features
- Utilize auto-imports for components and composables
- Use Nuxt's server middleware for API routes
- Consider using Nuxt Content module for content-heavy sites
- Utilize Nuxt's alias feature for cleaner imports
- Use Nuxt's runtime config for environment-specific variables
- Implement Nuxt's PWA module if needed
- Use Nuxt's build modules for extending the build process
- Implement Nuxt's dynamic imports for code splitting
- Utilize Nuxt's hooks for extending the Nuxt lifecycle
- Use Nuxt's extend webpack config for custom build configurations
- Implement Nuxt's loading component for better UX during page loads
- Use Nuxt's transition property for page transitions
- Utilize Nuxt's $config for accessing runtime config in components and pages
- Use Nuxt's generate.routes for dynamic route generation in static sites
- Implement Nuxt's webpackPreload for critical assets
- Use Nuxt's `asyncData` and `fetch` methods effectively
- Implement Nuxt's middleware for route-level functionality
- Utilize Nuxt's plugins system for extending application functionality
- Use Nuxt's `head` method for per-page SEO optimization
- Implement Nuxt's error handling for custom error pages
- Use Nuxt's `useFetch` composable for data fetching in components

## 10.15 Testing Best Practices
- Implement comprehensive unit testing for components and functions
- Use integration tests to ensure different parts of the application work together
- Implement end-to-end testing for critical user flows
- Use mocking for API calls and external dependencies in tests
- Implement continuous integration to run tests automatically

## 10.16 Documentation Best Practices
- Maintain clear and up-to-date documentation for the project
- Use JSDoc or similar tools for inline code documentation
- Document complex logic and algorithms
- Keep a changelog to track version changes

This comprehensive list of best practices covers various aspects of Vue 3 and Nuxt.js development, from code quality and performance optimization to specific Vue.js and Nuxt.js best practices. Implementing these practices will help in creating maintainable, efficient, and high-quality applications.

# 11. Ecosystem and Third-Party Integrations
- Explore and integrate relevant Vue.js plugins
- Consider using UI component libraries (e.g., Vuetify, Element Plus)
- Integrate with backend frameworks and APIs
- Explore state management alternatives (e.g., XState for complex state machines)
- Consider integrating static site generators (e.g., VuePress for documentation)
- Explore and integrate relevant Nuxt.js modules
- Consider integrating with headless CMS platforms
- Explore integrations with serverless platforms
- Consider integrating with e-commerce platforms
- Explore integrations with analytics tools
  - Google Analytics
  - Matomo
  - Custom analytics solutions
- Consider integrating with A/B testing platforms
  - Optimizely
  - VWO (Visual Website Optimizer)
  - Google Optimize
- Explore integrations with marketing automation tools
  - Mailchimp
  - HubSpot
  - Marketo
- Consider integrating with customer support platforms
  - Zendesk
  - Intercom
  - Freshdesk
- Explore integrations with monitoring and error tracking services
  - Sentry
  - LogRocket
  - New Relic
- Consider integrating with CI/CD platforms
  - Jenkins
  - GitLab CI
  - CircleCI
  - GitHub Actions
- Explore integrations with performance monitoring tools
  - Lighthouse CI
  - WebPageTest
  - SpeedCurve
- Consider integrating with payment gateways
  - Stripe
  - PayPal
  - Square
- Explore integrations with authentication providers
  - Auth0
  - Firebase Authentication
  - Okta
- Consider integrating with map services
  - Google Maps
  - Mapbox
  - OpenStreetMap
- Explore integrations with social media platforms
  - Facebook SDK
  - Twitter API
  - LinkedIn API
- Consider integrating with search engines
  - Algolia
  - Elasticsearch
  - MeiliSearch
- Explore integrations with file storage services
  - Amazon S3
  - Google Cloud Storage
  - Cloudinary
- Consider integrating with push notification services
  - Firebase Cloud Messaging
  - OneSignal
  - Pusher
- Explore integrations with A/I and machine learning services
  - TensorFlow.js
  - ml5.js
  - Azure Cognitive Services

# Conclusion

This comprehensive guide covers all aspects of Vue 3 and Nuxt.js development, from project initialization to advanced topics and ecosystem integrations. By following these best practices and exploring the various tools and techniques presented, you'll be well-equipped to build efficient, maintainable, and high-performance applications.

Remember that the Vue and Nuxt ecosystems are constantly evolving, so it's important to stay updated with the latest developments, releases, and community best practices. Regularly check the official documentation, participate in community forums, and explore new tools and libraries to keep your skills sharp and your projects cutting-edge.

As you develop your applications, always consider the specific needs of your project and users. Not every technique or integration will be necessary for every project, so use this guide as a reference to choose the most appropriate solutions for your unique challenges.

Finally, don't forget the importance of continuous learning and experimentation. The world of frontend development is always changing, and staying curious and open to new ideas will help you grow as a developer and create even better Vue and Nuxt applications in the future.

Happy coding!