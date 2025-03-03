.nuxt
Nuxt uses the .nuxt/ directory in development to generate your Vue application.
This directory should be added to your .gitignore file to avoid pushing the dev build output to your repository.
This directory is interesting if you want to learn more about the files Nuxt generates based on your directory structure.

Nuxt also provides a Virtual File System (VFS) for modules to add templates to this directory without writing them to disk.

You can explore the generated files by opening the Nuxt DevTools in development mode and navigating to the Virtual Files tab.

You should not touch any files inside since the whole directory will be re-created when running nuxt dev.

---

.output
Nuxt creates the .output/ directory when building your application for production.
This directory should be added to your .gitignore file to avoid pushing the build output to your repository.
Use this directory to deploy your Nuxt application to production.

 Read more in Docs > Getting Started > Deployment.
You should not touch any files inside since the whole directory will be re-created when running nuxt build.

---

assets
The assets/ directory is used to add all the website's assets that the build tool will process.
The directory usually contains the following types of files:

Stylesheets (CSS, SASS, etc.)
Fonts
Images that won't be served from the public/ directory.
If you want to serve assets from the server, we recommend taking a look at the public/ directory.

---

components
The components/ directory is where you put all your Vue components.
Nuxt automatically imports any components in this directory (along with components that are registered by any modules you may be using).

Directory Structure

-| components/
---| AppHeader.vue
---| AppFooter.vue
app.vue

<template>
  <div>
    <AppHeader />
    <NuxtPage />
    <AppFooter />
  </div>
</template>
Component Names
If you have a component in nested directories such as:

Directory Structure

-| components/
---| base/
-----| foo/
-------| Button.vue
... then the component's name will be based on its own path directory and filename, with duplicate segments being removed. Therefore, the component's name will be:


<BaseFooButton />
For clarity, we recommend that the component's filename matches its name. So, in the example above, you could rename Button.vue to be BaseFooButton.vue.
If you want to auto-import components based only on its name, not path, then you need to set pathPrefix option to false using extended form of the configuration object:

nuxt.config.ts

export default defineNuxtConfig({
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
});
This registers the components using the same strategy as used in Nuxt 2. For example, ~/components/Some/MyComponent.vue will be usable as <MyComponent> and not <SomeMyComponent>.

Dynamic Components
If you want to use the Vue <component :is="someComputedComponent"> syntax, you need to use the resolveComponent helper provided by Vue or import the component directly from #components and pass it into is prop.

For example:

pages/index.vue

<script setup lang="ts">
import { SomeComponent } from '#components'

const MyButton = resolveComponent('MyButton')
</script>

<template>
  <component :is="clickable ? MyButton : 'div'" />
  <component :is="SomeComponent" />
</template>
If you are using resolveComponent to handle dynamic components, make sure not to insert anything but the name of the component, which must be a string and not a variable.
Watch Daniel Roe's short video about resolveComponent.
Alternatively, though not recommended, you can register all your components globally, which will create async chunks for all your components and make them available throughout your application.


  export default defineNuxtConfig({
    components: {
+     global: true,
+     dirs: ['~/components']
    },
  })
You can also selectively register some components globally by placing them in a ~/components/global directory, or by using a .global.vue suffix in the filename. As noted above, each global component is rendered in a separate chunk, so be careful not to overuse this feature.

The global option can also be set per component directory.
Dynamic Imports
To dynamically import a component (also known as lazy-loading a component) all you need to do is add the Lazy prefix to the component's name. This is particularly useful if the component is not always needed.

By using the Lazy prefix you can delay loading the component code until the right moment, which can be helpful for optimizing your JavaScript bundle size.

pages/index.vue

<script setup lang="ts">
const show = ref(false)
</script>

<template>
  <div>
    <h1>Mountains</h1>
    <LazyMountainsList v-if="show" />
    <button v-if="!show" @click="show = true">Show List</button>
  </div>
</template>
Direct Imports
You can also explicitly import components from #components if you want or need to bypass Nuxt's auto-importing functionality.

pages/index.vue

<script setup lang="ts">
import { NuxtLink, LazyMountainsList } from '#components'

const show = ref(false)
</script>

<template>
  <div>
    <h1>Mountains</h1>
    <LazyMountainsList v-if="show" />
    <button v-if="!show" @click="show = true">Show List</button>
    <NuxtLink to="/">Home</NuxtLink>
  </div>
</template>
Custom Directories
By default, only the ~/components directory is scanned. If you want to add other directories, or change how the components are scanned within a subfolder of this directory, you can add additional directories to the configuration:

nuxt.config.ts

export default defineNuxtConfig({
  components: [
    // ~/calendar-module/components/event/Update.vue => <EventUpdate />
    { path: '~/calendar-module/components' },

    // ~/user-module/components/account/UserDeleteDialog.vue => <UserDeleteDialog />
    { path: '~/user-module/components', pathPrefix: false },

    // ~/components/special-components/Btn.vue => <SpecialBtn />
    { path: '~/components/special-components', prefix: 'Special' },

    // It's important that this comes last if you have overrides you wish to apply
    // to sub-directories of `~/components`.
    //
    // ~/components/Btn.vue => <Btn />
    // ~/components/base/Btn.vue => <BaseBtn />
    '~/components'
  ]
})
npm Packages
If you want to auto-import components from an npm package, you can use addComponent in a local module to register them.


~/modules/register-component.ts

app.vue

import { addComponent, defineNuxtModule } from '@nuxt/kit'

export default defineNuxtModule({
  setup() {
    // import { MyComponent as MyAutoImportedComponent } from 'my-npm-package'
    addComponent({
      name: 'MyAutoImportedComponent',
      export: 'MyComponent',
      filePath: 'my-npm-package',
    })
  },
})
Any nested directories need to be added first as they are scanned in order.
Component Extensions
By default, any file with an extension specified in the extensions key of nuxt.config.ts is treated as a component. If you need to restrict the file extensions that should be registered as components, you can use the extended form of the components directory declaration and its extensions key:

nuxt.config.ts

export default defineNuxtConfig({
  components: [
    {
      path: '~/components',
      extensions: ['.vue'],
    }
  ]
})
Client Components
If a component is meant to be rendered only client-side, you can add the .client suffix to your component.

Directory Structure

| components/
--| Comments.client.vue
pages/example.vue

<template>
  <div>
    <!-- this component will only be rendered on client side -->
    <Comments />
  </div>
</template>
This feature only works with Nuxt auto-imports and #components imports. Explicitly importing these components from their real paths does not convert them into client-only components.
.client components are rendered only after being mounted. To access the rendered template using onMounted(), add await nextTick() in the callback of the onMounted() hook.
You can also achieve a similar result with the <ClientOnly> component.
Server Components
Server components allow server-rendering individual components within your client-side apps. It's possible to use server components within Nuxt, even if you are generating a static site. That makes it possible to build complex sites that mix dynamic components, server-rendered HTML and even static chunks of markup.

Server components can either be used on their own or paired with a client component.

Watch Learn Vue video about Nuxt Server Components.
Read Daniel Roe's guide to Nuxt Server Components.
Standalone server components
Standalone server components will always be rendered on the server, also known as Islands components.

When their props update, this will result in a network request that will update the rendered HTML in-place.

Server components are currently experimental and in order to use them, you need to enable the 'component islands' feature in your nuxt.config:

nuxt.config.ts

export default defineNuxtConfig({
  experimental: {
    componentIslands: true
  }
})
Now you can register server-only components with the .server suffix and use them anywhere in your application automatically.

Directory Structure

-| components/
---| HighlightedMarkdown.server.vue
pages/example.vue

<template>
  <div>
    <!--
      this will automatically be rendered on the server, meaning your markdown parsing + highlighting
      libraries are not included in your client bundle.
     -->
    <HighlightedMarkdown markdown="# Headline" />
  </div>
</template>
Server-only components use <NuxtIsland> under the hood, meaning that lazy prop and #fallback slot are both passed down to it.

Server components (and islands) must have a single root element. (HTML comments are considered elements as well.)
Be careful when nesting islands within other islands as each island adds some extra overhead.
Most features for server-only components and island components, such as slots and client components, are only available for single file components.
Client components within server components
This feature needs experimental.componentIslands.selectiveClient within your configuration to be true.
You can partially hydrate a component by setting a nuxt-client attribute on the component you wish to be loaded client-side.

components/ServerWithClient.vue

<template>
  <div>
    <HighlightedMarkdown markdown="# Headline" />
    <!-- Counter will be loaded and hydrated client-side -->
    <Counter nuxt-client :count="5" />
  </div>
</template>
This only works within a server component. Slots for client components are working only with experimental.componentIsland.selectiveClient set to 'deep' and since they are rendered server-side, they are not interactive once client-side.
Server Component Context
When rendering a server-only or island component, <NuxtIsland> makes a fetch request which comes back with a NuxtIslandResponse. (This is an internal request if rendered on the server, or a request that you can see in the network tab if it's rendering on client-side navigation.)

This means:

A new Vue app will be created server-side to create the NuxtIslandResponse.
A new 'island context' will be created while rendering the component.
You can't access the 'island context' from the rest of your app and you can't access the context of the rest of your app from the island component. In other words, the server component or island is isolated from the rest of your app.
Your plugins will run again when rendering the island, unless they have env: { islands: false } set (which you can do in an object-syntax plugin).
Within an island component, you can access its island context through nuxtApp.ssrContext.islandContext. Note that while island components are still marked as experimental, the format of this context may change.

Slots can be interactive and are wrapped within a <div> with display: contents;
Paired with a Client component
In this case, the .server + .client components are two 'halves' of a component and can be used in advanced use cases for separate implementations of a component on server and client side.

Directory Structure

-| components/
---| Comments.client.vue
---| Comments.server.vue
pages/example.vue

<template>
  <div>
    <!-- this component will render Comments.server on the server then Comments.client once mounted in the browser -->
    <Comments />
  </div>
</template>
Built-In Nuxt Components
There are a number of components that Nuxt provides, including <ClientOnly> and <DevOnly>. You can read more about them in the API documentation.

 Read more in Docs > API.
Library Authors
Making Vue component libraries with automatic tree-shaking and component registration is super easy. ✨

You can use the components:dirs hook to extend the directory list without requiring user configuration in your Nuxt module.

Imagine a directory structure like this:

Directory Structure

-| node_modules/
---| awesome-ui/
-----| components/
-------| Alert.vue
-------| Button.vue
-----| nuxt.js
-| pages/
---| index.vue
-| nuxt.config.js
Then in awesome-ui/nuxt.js you can use the components:dirs hook:


import { defineNuxtModule, createResolver } from '@nuxt/kit'

export default defineNuxtModule({
  hooks: {
    'components:dirs': (dirs) => {
      const { resolve } = createResolver(import.meta.url)
      // Add ./components dir to the list
      dirs.push({
        path: resolve('./components'),
        prefix: 'awesome'
      })
    }
  }
})
That's it! Now in your project, you can import your UI library as a Nuxt module in your nuxt.config file:

nuxt.config.ts

export default defineNuxtConfig({
  modules: ['awesome-ui/nuxt']
})
... and directly use the module components (prefixed with awesome-) in our pages/index.vue:


<template>
  <div>
    My <AwesomeButton>UI button</AwesomeButton>!
    <awesome-alert>Here's an alert!</awesome-alert>
  </div>
</template>
It will automatically import the components only if used and also support HMR when updating your components in node_modules/awesome-ui/components/.

---

composables
Use the composables/ directory to auto-import your Vue composables into your application.
Usage
Method 1: Using named export

composables/useFoo.ts

export const useFoo = () => {
  return useState('foo', () => 'bar')
}
Method 2: Using default export

composables/use-foo.ts or composables/useFoo.ts

// It will be available as useFoo() (camelCase of file name without extension)
export default function () {
  return useState('foo', () => 'bar')
}
Usage: You can now use auto imported composable in .js, .ts and .vue files

app.vue

<script setup lang="ts">
const foo = useFoo()
</script>

<template>
  <div>
    {{ foo }}
  </div>
</template>
The composables/ directory in Nuxt does not provide any additional reactivity capabilities to your code. Instead, any reactivity within composables is achieved using Vue's Composition API mechanisms, such as ref and reactive. Note that reactive code is also not limited to the boundaries of the composables/ directory. You are free to employ reactivity features wherever they're needed in your application.
 Read more in Docs > Guide > Concepts > Auto Imports.
 Read and edit a live example in Docs > Examples > Features > Auto Imports.
Types
Under the hood, Nuxt auto generates the file .nuxt/imports.d.ts to declare the types.

Be aware that you have to run nuxi prepare, nuxi dev or nuxi build in order to let Nuxt generate the types.

If you create a composable without having the dev server running, TypeScript will throw an error, such as Cannot find name 'useBar'.
Examples
Nested Composables
You can use a composable within another composable using auto imports:

composables/test.ts

export const useFoo = () => {
  const nuxtApp = useNuxtApp()
  const bar = useBar()
}
Access plugin injections
You can access plugin injections from composables:

composables/test.ts

export const useHello = () => {
  const nuxtApp = useNuxtApp()
  return nuxtApp.$hello
}
How Files Are Scanned
Nuxt only scans files at the top level of the composables/ directory, e.g.:

Directory Structure

-| composables/
---| index.ts     // scanned
---| useFoo.ts    // scanned
---| nested/
-----| utils.ts   // not scanned
Only composables/index.ts and composables/useFoo.ts would be searched for imports.

To get auto imports working for nested modules, you could either re-export them (recommended) or configure the scanner to include nested directories:

Example: Re-export the composables you need from the composables/index.ts file:

composables/index.ts

// Enables auto import for this export
export { utils } from './nested/utils.ts'
Example: Scan nested directories inside the composables/ folder:

nuxt.config.ts

export default defineNuxtConfig({
  imports: {
    dirs: [
      // Scan top-level modules
      'composables',
      // ... or scan modules nested one level deep with a specific name and file extension
      'composables/*/index.{ts,js,mjs,mts}',
      // ... or scan all modules within given directory
      'composables/**'
    ]
  }
})

---

content
Use the content/ directory to create a file-based CMS for your application.
Nuxt Content reads the content/ directory in your project and parses .md, .yml, .csv and .json files to create a file-based CMS for your application.

Render your content with built-in components.
Query your content with a MongoDB-like API.
Use your Vue components in Markdown files with the MDC syntax.
Automatically generate your navigation.
Learn more in Nuxt Content documentation.
Enable Nuxt Content
Install the @nuxt/content module in your project as well as adding it to your nuxt.config.ts with one command:

Terminal

npx nuxi module add content
Create Content
Place your markdown files inside the content/ directory:

content/index.md

# Hello Content
The module automatically loads and parses them.

Render Content
To render content pages, add a catch-all route using the <ContentDoc> component:

pages/[...slug].vue

<template>
  <main>
    <!-- ContentDoc returns content for `$route.path` by default or you can pass a `path` prop -->
    <ContentDoc />
  </main>
</template>
Documentation

---

layouts
Nuxt provides a layouts framework to extract common UI patterns into reusable layouts.
For best performance, components placed in this directory will be automatically loaded via asynchronous import when used.
Enable Layouts
Layouts are enabled by adding <NuxtLayout> to your app.vue:

app.vue

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
To use a layout:

Set a layout property in your page with definePageMeta.
Set the name prop of <NuxtLayout>.
The layout name is normalized to kebab-case, so someLayout becomes some-layout.
If no layout is specified, layouts/default.vue will be used.
If you only have a single layout in your application, we recommend using app.vue instead.
Unlike other components, your layouts must have a single root element to allow Nuxt to apply transitions between layout changes - and this root element cannot be a <slot />.
Default Layout
Add a ~/layouts/default.vue:

layouts/default.vue

<template>
  <div>
    <p>Some default layout content shared across all pages</p>
    <slot />
  </div>
</template>
In a layout file, the content of the page will be displayed in the <slot /> component.

Named Layout
Directory Structure

-| layouts/
---| default.vue
---| custom.vue
Then you can use the custom layout in your page:

pages/about.vue

<script setup lang="ts">
definePageMeta({
  layout: 'custom'
})
</script>
Learn more about definePageMeta.
You can directly override the default layout for all pages using the name property of <NuxtLayout>:

app.vue

<script setup lang="ts">
// You might choose this based on an API call or logged-in status
const layout = "custom";
</script>

<template>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>
If you have a layout in nested directories, the layout's name will be based on its own path directory and filename, with duplicate segments being removed.

File	Layout Name
~/layouts/desktop/default.vue	desktop-default
~/layouts/desktop-base/base.vue	desktop-base
~/layouts/desktop/index.vue	desktop
For clarity, we recommend that the layout's filename matches its name:

File	Layout Name
~/layouts/desktop/DesktopDefault.vue	desktop-default
~/layouts/desktop-base/DesktopBase.vue	desktop-base
~/layouts/desktop/Desktop.vue	desktop
 Read and edit a live example in Docs > Examples > Features > Layouts.
Changing the Layout Dynamically
You can also use the setPageLayout helper to change the layout dynamically:


<script setup lang="ts">
function enableCustomLayout () {
  setPageLayout('custom')
}
definePageMeta({
  layout: false,
});
</script>

<template>
  <div>
    <button @click="enableCustomLayout">Update layout</button>
  </div>
</template>
 Read and edit a live example in Docs > Examples > Features > Layouts.
Overriding a Layout on a Per-page Basis
If you are using pages, you can take full control by setting layout: false and then using the <NuxtLayout> component within the page.


pages/index.vue

layouts/custom.vue

<script setup lang="ts">
definePageMeta({
  layout: false,
})
</script>

<template>
  <div>
    <NuxtLayout name="custom">
      <template #header> Some header template content. </template>

      The rest of the page
    </NuxtLayout>
  </div>
</template>
If you use <NuxtLayout> within your pages, make sure it is not the root element (or disable layout/page transitions).

---

middleware
Nuxt provides middleware to run code before navigating to a particular route.
Nuxt provides a customizable route middleware framework you can use throughout your application, ideal for extracting code that you want to run before navigating to a particular route.

There are three kinds of route middleware:

Anonymous (or inline) route middleware are defined directly within the page.
Named route middleware, placed in the middleware/ and automatically loaded via asynchronous import when used on a page.
Global route middleware, placed in the middleware/ with a .global suffix and is run on every route change.
The first two kinds of route middleware can be defined in definePageMeta.

Name of middleware are normalized to kebab-case: myMiddleware becomes my-middleware.
Route middleware run within the Vue part of your Nuxt app. Despite the similar name, they are completely different from server middleware, which are run in the Nitro server part of your app.
Usage
Route middleware are navigation guards that receive the current route and the next route as arguments.

middleware/my-middleware.ts

export default defineNuxtRouteMiddleware((to, from) => {
  if (to.params.id === '1') {
    return abortNavigation()
  }
  // In a real app you would probably not redirect every route to `/`
  // however it is important to check `to.path` before redirecting or you
  // might get an infinite redirect loop
  if (to.path !== '/') {
    return navigateTo('/')
  }
})
Nuxt provides two globally available helpers that can be returned directly from the middleware.

navigateTo - Redirects to the given route
abortNavigation - Aborts the navigation, with an optional error message.
Unlike navigation guards from vue-router, a third next() argument is not passed, and redirect or route cancellation is handled by returning a value from the middleware.

Possible return values are:

nothing (a simple return or no return at all) - does not block navigation and will move to the next middleware function, if any, or complete the route navigation
return navigateTo('/') - redirects to the given path and will set the redirect code to 302 Found if the redirect happens on the server side
return navigateTo('/', { redirectCode: 301 }) - redirects to the given path and will set the redirect code to 301 Moved Permanently if the redirect happens on the server side
return abortNavigation() - stops the current navigation
return abortNavigation(error) - rejects the current navigation with an error
 Read more in Docs > API > Utils > Navigate To.
 Read more in Docs > API > Utils > Abort Navigation.
We recommend using the helper functions above for performing redirects or stopping navigation. Other possible return values described in the vue-router docs may work but there may be breaking changes in future.
Middleware Order
Middleware runs in the following order:

Global Middleware
Page defined middleware order (if there are multiple middleware declared with the array syntax)
For example, assuming you have the following middleware and component:

middleware/ directory

-| middleware/
---| analytics.global.ts
---| setup.global.ts
---| auth.ts
pages/profile.vue

<script setup lang="ts">
definePageMeta({
  middleware: [
    function (to, from) {
      // Custom inline middleware
    },
    'auth',
  ],
});
</script>
You can expect the middleware to be run in the following order:

analytics.global.ts
setup.global.ts
Custom inline middleware
auth.ts
Ordering Global Middleware
By default, global middleware is executed alphabetically based on the filename.

However, there may be times you want to define a specific order. For example, in the last scenario, setup.global.ts may need to run before analytics.global.ts. In that case, we recommend prefixing global middleware with 'alphabetical' numbering.

Directory structure

-| middleware/
---| 01.setup.global.ts
---| 02.analytics.global.ts
---| auth.ts
In case you're new to 'alphabetical' numbering, remember that filenames are sorted as strings, not as numeric values. For example, 10.new.global.ts would come before 2.new.global.ts. This is why the example prefixes single digit numbers with 0.
When Middleware Runs
If your site is server-rendered or generated, middleware for the initial page will be executed both when the page is rendered and then again on the client. This might be needed if your middleware needs a browser environment, such as if you have a generated site, aggressively cache responses, or want to read a value from local storage.

However, if you want to avoid this behaviour you can do so:

middleware/example.ts

export default defineNuxtRouteMiddleware(to => {
  // skip middleware on server
  if (import.meta.server) return
  // skip middleware on client side entirely
  if (import.meta.client) return
  // or only skip middleware on initial client load
  const nuxtApp = useNuxtApp()
  if (import.meta.client && nuxtApp.isHydrating && nuxtApp.payload.serverRendered) return
})
Rendering an error page is an entirely separate page load, meaning any registered middleware will run again. You can use useError in middleware to check if an error is being handled.
Adding Middleware Dynamically
It is possible to add global or named route middleware manually using the addRouteMiddleware() helper function, such as from within a plugin.


export default defineNuxtPlugin(() => {
  addRouteMiddleware('global-test', () => {
    console.log('this global middleware was added in a plugin and will be run on every route change')
  }, { global: true })

  addRouteMiddleware('named-test', () => {
    console.log('this named middleware was added in a plugin and would override any existing middleware of the same name')
  })
})
Example
Directory Structure

-| middleware/
---| auth.ts
In your page file, you can reference this route middleware:


<script setup lang="ts">
definePageMeta({
  middleware: ["auth"]
  // or middleware: 'auth'
})
</script>
Now, before navigation to that page can complete, the auth route middleware will be run.

 Read and edit a live example in Docs > Examples > Routing > Middleware.
Setting Middleware At Build Time
Instead of using definePageMeta on each page, you can add named route middleware within the pages:extend hook.

nuxt.config.ts

import type { NuxtPage } from 'nuxt/schema'

export default defineNuxtConfig({
  hooks: {
    'pages:extend' (pages) {
      function setMiddleware (pages: NuxtPage[]) {
        for (const page of pages) {
          if (/* some condition */ true) {
            page.meta ||= {}
            // Note that this will override any middleware set in `definePageMeta` in the page
            page.meta.middleware = ['named']
          }
          if (page.children) {
            setMiddleware(page.children)
          }
        }
      }
      setMiddleware(pages)
    }
  }
})

---

modules
Use the modules/ directory to automatically register local modules within your application.
It is a good place to place any local modules you develop while building your application.

The auto-registered files patterns are:

modules/*/index.ts
modules/*.ts
You don't need to add those local modules to your nuxt.config.ts separately.


modules/hello/index.ts

modules/hello/runtime/api-route.ts

// `nuxt/kit` is a helper subpath import you can use when defining local modules
// that means you do not need to add `@nuxt/kit` to your project's dependencies
import { createResolver, defineNuxtModule, addServerHandler } from 'nuxt/kit'

export default defineNuxtModule({
  meta: {
    name: 'hello'
  },
  setup () {
    const { resolve } = createResolver(import.meta.url)

    // Add an API route
    addServerHandler({
      route: '/api/hello',
      handler: resolve('./runtime/api-route')
    })
  }
})
When starting Nuxt, the hello module will be registered and the /api/hello route will be available.

Modules are executed in the following sequence:

First, the modules defined in nuxt.config.ts are loaded.
Then, modules found in the modules/ directory are executed, and they load in alphabetical order.
You can change the order of local module by adding a number to the front of each directory name:

Directory structure

modules/
  1.first-module/
    index.ts
  2.second-module.ts

---

pages
Nuxt provides file-based routing to create routes within your web application.
To reduce your application's bundle size, this directory is optional, meaning that vue-router won't be included if you only use app.vue. To force the pages system, set pages: true in nuxt.config or have a app/router.options.ts.
Usage
Pages are Vue components and can have any valid extension that Nuxt supports (by default .vue, .js, .jsx, .mjs, .ts or .tsx).

Nuxt will automatically create a route for every page in your ~/pages/ directory.


pages/index.vue

pages/index.ts

pages/index.tsx

<template>
  <h1>Index page</h1>
</template>
The pages/index.vue file will be mapped to the / route of your application.

If you are using app.vue, make sure to use the <NuxtPage/> component to display the current page:

app.vue

<template>
  <div>
    <!-- Markup shared across all pages, ex: NavBar -->
    <NuxtPage />
  </div>
</template>
Pages must have a single root element to allow route transitions between pages. HTML comments are considered elements as well.

This means that when the route is server-rendered, or statically generated, you will be able to see its contents correctly, but when you navigate towards that route during client-side navigation the transition between routes will fail and you'll see that the route will not be rendered.

Here are some examples to illustrate what a page with a single root element looks like:


pages/working.vue

pages/bad-1.vue

pages/bad-2.vue

<template>
  <div>
    <!-- This page correctly has only one single root element -->
    Page content
  </div>
</template>
Dynamic Routes
If you place anything within square brackets, it will be turned into a dynamic route parameter. You can mix and match multiple parameters and even non-dynamic text within a file name or directory.

If you want a parameter to be optional, you must enclose it in double square brackets - for example, ~/pages/[[slug]]/index.vue or ~/pages/[[slug]].vue will match both / and /test.

Directory Structure

-| pages/
---| index.vue
---| users-[group]/
-----| [id].vue
Given the example above, you can access group/id within your component via the $route object:

pages/users-[group]/[id].vue

<template>
  <p>{{ $route.params.group }} - {{ $route.params.id }}</p>
</template>
Navigating to /users-admins/123 would render:


<p>admins - 123</p>
If you want to access the route using Composition API, there is a global useRoute function that will allow you to access the route just like this.$route in the Options API.


<script setup lang="ts">
const route = useRoute()

if (route.params.group === 'admins' && !route.params.id) {
  console.log('Warning! Make sure user is authenticated!')
}
</script>
Named parent routes will take priority over nested dynamic routes. For the /foo/hello route, ~/pages/foo.vue will take priority over ~/pages/foo/[slug].vue.
Use ~/pages/foo/index.vue and ~/pages/foo/[slug].vue to match /foo and /foo/hello with different pages,.
Catch-all Route
If you need a catch-all route, you create it by using a file named like [...slug].vue. This will match all routes under that path.

pages/[...slug].vue

<template>
  <p>{{ $route.params.slug }}</p>
</template>
Navigating to /hello/world would render:


<p>["hello", "world"]</p>
Nested Routes
It is possible to display nested routes with <NuxtPage>.

Example:

Directory Structure

-| pages/
---| parent/
-----| child.vue
---| parent.vue
This file tree will generate these routes:


[
  {
    path: '/parent',
    component: '~/pages/parent.vue',
    name: 'parent',
    children: [
      {
        path: 'child',
        component: '~/pages/parent/child.vue',
        name: 'parent-child'
      }
    ]
  }
]
To display the child.vue component, you have to insert the <NuxtPage> component inside pages/parent.vue:

pages/parent.vue

<template>
  <div>
    <h1>I am the parent view</h1>
    <NuxtPage :foobar="123" />
  </div>
</template>
pages/parent/child.vue

<script setup lang="ts">
const props = defineProps(['foobar'])

console.log(props.foobar)
</script>
Child Route Keys
If you want more control over when the <NuxtPage> component is re-rendered (for example, for transitions), you can either pass a string or function via the pageKey prop, or you can define a key value via definePageMeta:

pages/parent.vue

<template>
  <div>
    <h1>I am the parent view</h1>
    <NuxtPage :page-key="route => route.fullPath" />
  </div>
</template>
Or alternatively:

pages/parent/child.vue

<script setup lang="ts">
definePageMeta({
  key: route => route.fullPath
})
</script>
 Read and edit a live example in Docs > Examples > Routing > Pages.
Route Groups
In some cases, you may want to group a set of routes together in a way which doesn't affect file-based routing. For this purpose, you can put files in a folder which is wrapped in parentheses - ( and ).

For example:

Directory structure

-| pages/
---| index.vue
---| (marketing)/
-----| about.vue
-----| contact.vue
This will produce /, /about and /contact pages in your app. The marketing group is ignored for purposes of your URL structure.

Page Metadata
You might want to define metadata for each route in your app. You can do this using the definePageMeta macro, which will work both in <script> and in <script setup>:


<script setup lang="ts">
definePageMeta({
  title: 'My home page'
})
</script>
This data can then be accessed throughout the rest of your app from the route.meta object.


<script setup lang="ts">
const route = useRoute()

console.log(route.meta.title) // My home page
</script>
If you are using nested routes, the page metadata from all these routes will be merged into a single object. For more on route meta, see the vue-router docs.

Much like defineEmits or defineProps (see Vue docs), definePageMeta is a compiler macro. It will be compiled away so you cannot reference it within your component. Instead, the metadata passed to it will be hoisted out of the component. Therefore, the page meta object cannot reference the component. However, it can reference imported bindings, as well as locally defined pure functions.

Make sure not to reference any reactive data or functions that cause side effects. This can lead to unexpected behavior.

<script setup lang="ts">
import { someData } from '~/utils/example'

function validateIdParam(route) {
  return route.params.id && !isNaN(Number(route.params.id))
}

const title = ref('')

definePageMeta({
  validate: validateIdParam,
  someData,
  title,    // do not do this, the ref will be hoisted out of the component
})
</script>
Special Metadata
Of course, you are welcome to define metadata for your own use throughout your app. But some metadata defined with definePageMeta has a particular purpose:

alias
You can define page aliases. They allow you to access the same page from different paths. It can be either a string or an array of strings as defined here on vue-router documentation.

keepalive
Nuxt will automatically wrap your page in the Vue <KeepAlive> component if you set keepalive: true in your definePageMeta. This might be useful to do, for example, in a parent route that has dynamic child routes, if you want to preserve page state across route changes.

When your goal is to preserve state for parent routes use this syntax: <NuxtPage keepalive />. You can also set props to be passed to <KeepAlive> (see a full list here).

You can set a default value for this property in your nuxt.config.

key
See above.

layout
You can define the layout used to render the route. This can be either false (to disable any layout), a string or a ref/computed, if you want to make it reactive in some way. More about layouts.

layoutTransition and pageTransition
You can define transition properties for the <transition> component that wraps your pages and layouts, or pass false to disable the <transition> wrapper for that route. You can see a list of options that can be passed here or read more about how transitions work.

You can set default values for these properties in your nuxt.config.

middleware
You can define middleware to apply before loading this page. It will be merged with all the other middleware used in any matching parent/child routes. It can be a string, a function (an anonymous/inlined middleware function following the global before guard pattern), or an array of strings/functions. More about named middleware.

name
You may define a name for this page's route.

path
You may define a path matcher, if you have a more complex pattern than can be expressed with the file name. See the vue-router docs for more information.

Typing Custom Metadata
If you add custom metadata for your pages, you may wish to do so in a type-safe way. It is possible to augment the type of the object accepted by definePageMeta:

index.d.ts

declare module '#app' {
  interface PageMeta {
    pageType?: string
  }
}

// It is always important to ensure you import/export something when augmenting a type
export {}
Navigation
To navigate between pages of your app, you should use the <NuxtLink> component.

This component is included with Nuxt and therefore you don't have to import it as you do with other components.

A simple link to the index.vue page in your pages folder:


<template>
  <NuxtLink to="/">Home page</NuxtLink>
</template>
Learn more about <NuxtLink> usage.
Programmatic Navigation
Nuxt allows programmatic navigation through the navigateTo() utility method. Using this utility method, you will be able to programmatically navigate the user in your app. This is great for taking input from the user and navigating them dynamically throughout your application. In this example, we have a simple method called navigate() that gets called when the user submits a search form.

Ensure to always await on navigateTo or chain its result by returning from functions.

<script setup lang="ts">
const name = ref('');
const type = ref(1);

function navigate(){
  return navigateTo({
    path: '/search',
    query: {
      name: name.value,
      type: type.value
    }
  })
}
</script>
Client-Only Pages
You can define a page as client only by giving it a .client.vue suffix. None of the content of this page will be rendered on the server.

Server-Only Pages
You can define a page as server only by giving it a .server.vue suffix. While you will be able to navigate to the page using client-side navigation, controlled by vue-router, it will be rendered with a server component automatically, meaning the code required to render the page will not be in your client-side bundle.

Server-only pages must have a single root element. (HTML comments are considered elements as well.)
Custom Routing
As your app gets bigger and more complex, your routing might require more flexibility. For this reason, Nuxt directly exposes the router, routes and router options for customization in different ways.

 Read more in Docs > Guide > Recipes > Custom Routing.
Multiple Pages Directories
By default, all your pages should be in one pages directory at the root of your project.

However, you can use Nuxt Layers to create groupings of your app's pages:

Directory Structure

-| some-app/
---| nuxt.config.ts
---| pages/
-----| app-page.vue
-| nuxt.config.ts
some-app/nuxt.config.ts

// some-app/nuxt.config.ts
export default defineNuxtConfig({
})
nuxt.config.ts

export default defineNuxtConfig({
  extends: ['./some-app'],
})

---

plugins
Nuxt has a plugins system to use Vue plugins and more at the creation of your Vue application.
Nuxt automatically reads the files in the plugins/ directory and loads them at the creation of the Vue application.

All plugins inside are auto-registered, you don't need to add them to your nuxt.config separately.
You can use .server or .client suffix in the file name to load a plugin only on the server or client side.
Registered Plugins
Only files at the top level of the directory (or index files within any subdirectories) will be auto-registered as plugins.

Directory structure

-| plugins/
---| foo.ts      // scanned
---| bar/
-----| baz.ts    // not scanned
-----| foz.vue   // not scanned
-----| index.ts  // currently scanned but deprecated
Only foo.ts and bar/index.ts would be registered.

To add plugins in subdirectories, you can use the plugins option in nuxt.config.ts:

nuxt.config.ts

export default defineNuxtConfig({
  plugins: [
    '~/plugins/bar/baz',
    '~/plugins/bar/foz'
  ]
})
Creating Plugins
The only argument passed to a plugin is nuxtApp.

plugins/hello.ts

export default defineNuxtPlugin(nuxtApp => {
  // Doing something with nuxtApp
})
Object Syntax Plugins
It is also possible to define a plugin using an object syntax, for more advanced use cases. For example:

plugins/hello.ts

export default defineNuxtPlugin({
  name: 'my-plugin',
  enforce: 'pre', // or 'post'
  async setup (nuxtApp) {
    // this is the equivalent of a normal functional plugin
  },
  hooks: {
    // You can directly register Nuxt app runtime hooks here
    'app:created'() {
      const nuxtApp = useNuxtApp()
      // do something in the hook
    }
  },
  env: {
    // Set this value to `false` if you don't want the plugin to run when rendering server-only or island components.
    islands: true
  }
})
Watch a video from Alexander Lichter about the Object Syntax for Nuxt plugins.
If you are using the object-syntax, the properties are statically analyzed to produce a more optimized build. So you should not define them at runtime.
For example, setting enforce: import.meta.server ? 'pre' : 'post' would defeat any future optimization Nuxt is able to do for your plugins. Nuxt does statically pre-load any hook listeners when using object-syntax, allowing you to define hooks without needing to worry about order of plugin registration.
Registration Order
You can control the order in which plugins are registered by prefixing with 'alphabetical' numbering to the file names.

Directory structure

plugins/
 | - 01.myPlugin.ts
 | - 02.myOtherPlugin.ts
In this example, 02.myOtherPlugin.ts will be able to access anything that was injected by 01.myPlugin.ts.

This is useful in situations where you have a plugin that depends on another plugin.

In case you're new to 'alphabetical' numbering, remember that filenames are sorted as strings, not as numeric values. For example, 10.myPlugin.ts would come before 2.myOtherPlugin.ts. This is why the example prefixes single digit numbers with 0.
Loading Strategy
Parallel Plugins
By default, Nuxt loads plugins sequentially. You can define a plugin as parallel so Nuxt won't wait until the end of the plugin's execution before loading the next plugin.

plugins/my-plugin.ts

export default defineNuxtPlugin({
  name: 'my-plugin',
  parallel: true,
  async setup (nuxtApp) {
    // the next plugin will be executed immediately
  }
})
Plugins With Dependencies
If a plugin needs to wait for another plugin before it runs, you can add the plugin's name to the dependsOn array.

plugins/depending-on-my-plugin.ts

export default defineNuxtPlugin({
  name: 'depends-on-my-plugin',
  dependsOn: ['my-plugin'],
  async setup (nuxtApp) {
    // this plugin will wait for the end of `my-plugin`'s execution before it runs
  }
})
Using Composables
You can use composables as well as utils within Nuxt plugins:

plugins/hello.ts

export default defineNuxtPlugin((nuxtApp) => {
  const foo = useFoo()
})
However, keep in mind there are some limitations and differences:

If a composable depends on another plugin registered later, it might not work.
Plugins are called in order sequentially and before everything else. You might use a composable that depends on another plugin which has not been called yet.
If a composable depends on the Vue.js lifecycle, it won't work.
Normally, Vue.js composables are bound to the current component instance while plugins are only bound to nuxtApp instance.
Providing Helpers
If you would like to provide a helper on the NuxtApp instance, return it from the plugin under a provide key.


plugins/hello.ts

plugins/hello-object-syntax.ts

export default defineNuxtPlugin(() => {
  return {
    provide: {
      hello: (msg: string) => `Hello ${msg}!`
    }
  }
})
You can then use the helper in your components:

components/Hello.vue

<script setup lang="ts">
// alternatively, you can also use it here
const { $hello } = useNuxtApp()
</script>

<template>
  <div>
    {{ $hello('world') }}
  </div>
</template>
Note that we highly recommend using composables instead of providing helpers to avoid polluting the global namespace and keep your main bundle entry small.
If your plugin provides a ref or computed, it will not be unwrapped in a component <template>.
This is due to how Vue works with refs that aren't top-level to the template. You can read more about it in the Vue documentation.
Typing Plugins
If you return your helpers from the plugin, they will be typed automatically; you'll find them typed for the return of useNuxtApp() and within your templates.

If you need to use a provided helper within another plugin, you can call useNuxtApp() to get the typed version. But in general, this should be avoided unless you are certain of the plugins' order.
For advanced use-cases, you can declare the type of injected properties like this:

index.d.ts

declare module '#app' {
  interface NuxtApp {
    $hello (msg: string): string
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $hello (msg: string): string
  }
}

export {}
If you are using WebStorm, you may need to augment @vue/runtime-core until this issue is resolved.
Vue Plugins
If you want to use Vue plugins, like vue-gtag to add Google Analytics tags, you can use a Nuxt plugin to do so.

First, install the Vue plugin dependency:


npm

yarn

pnpm

bun

npm install --save-dev vue-gtag-next
Then create a plugin file:

plugins/vue-gtag.client.ts

import VueGtag, { trackRouter } from 'vue-gtag-next'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueGtag, {
    property: {
      id: 'GA_MEASUREMENT_ID'
    }
  })
  trackRouter(useRouter())
})
Vue Directives
Similarly, you can register a custom Vue directive in a plugin.

plugins/my-directive.ts

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('focus', {
    mounted (el) {
      el.focus()
    },
    getSSRProps (binding, vnode) {
      // you can provide SSR-specific props here
      return {}
    }
  })
})
If you register a Vue directive, you must register it on both client and server side unless you are only using it when rendering one side. If the directive only makes sense from a client side, you can always move it to ~/plugins/my-directive.client.ts and provide a 'stub' directive for the server in ~/plugins/my-directive.server.ts.

---

public
The public/ directory is used to serve your website's static assets.
Files contained within the public/ directory are served at the root and are not modified by the build process. This is suitable for files that have to keep their names (e.g. robots.txt) or likely won't change (e.g. favicon.ico).

Directory structure

-| public/
---| favicon.ico
---| og-image.png
---| robots.txt
app.vue

<script setup lang="ts">
useSeoMeta({
  ogImage: '/og-image.png'
})
</script>

---

server
The server/ directory is used to register API and server handlers to your application.
Nuxt automatically scans files inside these directories to register API and server handlers with Hot Module Replacement (HMR) support.

Directory structure

-| server/
---| api/
-----| hello.ts      # /api/hello
---| routes/
-----| bonjour.ts    # /bonjour
---| middleware/
-----| log.ts        # log all requests
Each file should export a default function defined with defineEventHandler() or eventHandler() (alias).

The handler can directly return JSON data, a Promise, or use event.node.res.end() to send a response.

server/api/hello.ts

export default defineEventHandler((event) => {
  return {
    hello: 'world'
  }
})
You can now universally call this API in your pages and components:

pages/index.vue

<script setup lang="ts">
const { data } = await useFetch('/api/hello')
</script>

<template>
  <pre>{{ data }}</pre>
</template>
Server Routes
Files inside the ~/server/api are automatically prefixed with /api in their route.

To add server routes without /api prefix, put them into ~/server/routes directory.

Example:

server/routes/hello.ts

export default defineEventHandler(() => 'Hello World!')
Given the example above, the /hello route will be accessible at http://localhost:3000/hello.

Note that currently server routes do not support the full functionality of dynamic routes as pages do.
Server Middleware
Nuxt will automatically read in any file in the ~/server/middleware to create server middleware for your project.

Middleware handlers will run on every request before any other server route to add or check headers, log requests, or extend the event's request object.

Middleware handlers should not return anything (nor close or respond to the request) and only inspect or extend the request context or throw an error.
Examples:

server/middleware/log.ts

export default defineEventHandler((event) => {
  console.log('New request: ' + getRequestURL(event))
})
server/middleware/auth.ts

export default defineEventHandler((event) => {
  event.context.auth = { user: 123 }
})
Server Plugins
Nuxt will automatically read any files in the ~/server/plugins directory and register them as Nitro plugins. This allows extending Nitro's runtime behavior and hooking into lifecycle events.

Example:

server/plugins/nitroPlugin.ts

export default defineNitroPlugin((nitroApp) => {
  console.log('Nitro plugin', nitroApp)
})
 Read more in Nitro Plugins.
Server Utilities
Server routes are powered by unjs/h3 which comes with a handy set of helpers.

 Read more in Available H3 Request Helpers.
You can add more helpers yourself inside the ~/server/utils directory.

For example, you can define a custom handler utility that wraps the original handler and performs additional operations before returning the final response.

Example:

server/utils/handler.ts

import type { EventHandler, EventHandlerRequest } from 'h3'

export const defineWrappedResponseHandler = <T extends EventHandlerRequest, D> (
  handler: EventHandler<T, D>
): EventHandler<T, D> =>
  defineEventHandler<T>(async event => {
    try {
      // do something before the route handler
      const response = await handler(event)
      // do something after the route handler
      return { response }
    } catch (err) {
      // Error handling
      return { err }
    }
  })
Server Types
This feature is available from Nuxt >= 3.5
To improve clarity within your IDE between the auto-imports from 'nitro' and 'vue', you can add a ~/server/tsconfig.json with the following content:

server/tsconfig.json

{
  "extends": "../.nuxt/tsconfig.server.json"
}
Currently, these values won't be respected when type checking (nuxi typecheck), but you should get better type hints in your IDE.

Recipes
Route Parameters
Server routes can use dynamic parameters within brackets in the file name like /api/hello/[name].ts and be accessed via event.context.params.

server/api/hello/[name].ts

export default defineEventHandler((event) => {
  const name = getRouterParam(event, 'name')

  return `Hello, ${name}!`
})
Alternatively, use getValidatedRouterParams with a schema validator such as Zod for runtime and type safety.
You can now universally call this API on /api/hello/nuxt and get Hello, nuxt!.

Matching HTTP Method
Handle file names can be suffixed with .get, .post, .put, .delete, ... to match request's HTTP Method.

server/api/test.get.ts

export default defineEventHandler(() => 'Test get handler')
server/api/test.post.ts

export default defineEventHandler(() => 'Test post handler')
Given the example above, fetching /test with:

GET method: Returns Test get handler
POST method: Returns Test post handler
Any other method: Returns 405 error
You can also use index.[method].ts inside a directory for structuring your code differently, this is useful to create API namespaces.


server/api/foo/index.get.ts

server/api/foo/index.post.ts

server/api/foo/bar.get.ts

export default defineEventHandler((event) => {
  // handle GET requests for the `api/foo` endpoint
})
Catch-all Route
Catch-all routes are helpful for fallback route handling.

For example, creating a file named ~/server/api/foo/[...].ts will register a catch-all route for all requests that do not match any route handler, such as /api/foo/bar/baz.

server/api/foo/[...].ts

export default defineEventHandler((event) => {
  // event.context.path to get the route path: '/api/foo/bar/baz'
  // event.context.params._ to get the route segment: 'bar/baz'
  return `Default foo handler`
})
You can set a name for the catch-all route by using ~/server/api/foo/[...slug].ts and access it via event.context.params.slug.

server/api/foo/[...slug].ts

export default defineEventHandler((event) => {
  // event.context.params.slug to get the route segment: 'bar/baz'
  return `Default foo handler`
})
Body Handling
server/api/submit.post.ts

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  return { body }
})
Alternatively, use readValidatedBody with a schema validator such as Zod for runtime and type safety.
You can now universally call this API using:

app.vue

<script setup lang="ts">
async function submit() {
  const { body } = await $fetch('/api/submit', {
    method: 'post',
    body: { test: 123 }
  })
}
</script>
We are using submit.post.ts in the filename only to match requests with POST method that can accept the request body. When using readBody within a GET request, readBody will throw a 405 Method Not Allowed HTTP error.
Query Parameters
Sample query /api/query?foo=bar&baz=qux

server/api/query.get.ts

export default defineEventHandler((event) => {
  const query = getQuery(event)

  return { a: query.foo, b: query.baz }
})
Alternatively, use getValidatedQuery with a schema validator such as Zod for runtime and type safety.
Error Handling
If no errors are thrown, a status code of 200 OK will be returned.

Any uncaught errors will return a 500 Internal Server Error HTTP Error.

To return other error codes, throw an exception with createError:

server/api/validation/[id].ts

export default defineEventHandler((event) => {
  const id = parseInt(event.context.params.id) as number

  if (!Number.isInteger(id)) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID should be an integer',
    })
  }
  return 'All good'
})
Status Codes
To return other status codes, use the setResponseStatus utility.

For example, to return 202 Accepted

server/api/validation/[id].ts

export default defineEventHandler((event) => {
  setResponseStatus(event, 202)
})
Runtime Config

server/api/foo.ts

nuxt.config.ts

.env

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)

  const repo = await $fetch('https://api.github.com/repos/nuxt/nuxt', {
    headers: {
      Authorization: `token ${config.githubToken}`
    }
  })

  return repo
})
Giving the event as argument to useRuntimeConfig is optional, but it is recommended to pass it to get the runtime config overwritten by environment variables at runtime for server routes.
Request Cookies
server/api/cookies.ts

export default defineEventHandler((event) => {
  const cookies = parseCookies(event)

  return { cookies }
})
Forwarding Context & Headers
By default, neither the headers from the incoming request nor the request context are forwarded when making fetch requests in server routes. You can use event.$fetch to forward the request context and headers when making fetch requests in server routes.

server/api/forward.ts

export default defineEventHandler((event) => {
  return event.$fetch('/api/forwarded')
})
Headers that are not meant to be forwarded will not be included in the request. These headers include, for example: transfer-encoding, connection, keep-alive, upgrade, expect, host, accept
Awaiting Promises After Response
When handling server requests, you might need to perform asynchronous tasks that shouldn't block the response to the client (for example, caching and logging). You can use event.waitUntil to await a promise in the background without delaying the response.

The event.waitUntil method accepts a promise that will be awaited before the handler terminates, ensuring the task is completed even if the server would otherwise terminate the handler right after the response is sent. This integrates with runtime providers to leverage their native capabilities for handling asynchronous operations after the response is sent.

server/api/background-task.ts

const timeConsumingBackgroundTask = async () => {
  await new Promise((resolve) => setTimeout(resolve, 1000))
};

export default eventHandler((event) => {
  // schedule a background task without blocking the response
  event.waitUntil(timeConsumingBackgroundTask())

  // immediately send the response to the client
  return 'done'
});
Advanced Usage
Nitro Config
You can use nitro key in nuxt.config to directly set Nitro configuration.

This is an advanced option. Custom config can affect production deployments, as the configuration interface might change over time when Nitro is upgraded in semver-minor versions of Nuxt.
nuxt.config.ts

export default defineNuxtConfig({
  // https://nitro.unjs.io/config
  nitro: {}
})
 Read more in Docs > Guide > Concepts > Server Engine.
Nested Router
server/api/hello/[...slug].ts

import { createRouter, defineEventHandler, useBase } from 'h3'

const router = createRouter()

router.get('/test', defineEventHandler(() => 'Hello World'))

export default useBase('/api/hello', router.handler)
Sending Streams
This is an experimental feature and is available in all environments.
server/api/foo.get.ts

import fs from 'node:fs'
import { sendStream } from 'h3'

export default defineEventHandler((event) => {
  return sendStream(event, fs.createReadStream('/path/to/file'))
})
Sending Redirect
server/api/foo.get.ts

export default defineEventHandler(async (event) => {
  await sendRedirect(event, '/path/redirect/to', 302)
})
Legacy Handler or Middleware
server/api/legacy.ts

export default fromNodeMiddleware((req, res) => {
  res.end('Legacy handler')
})
Legacy support is possible using unjs/h3, but it is advised to avoid legacy handlers as much as you can.
server/middleware/legacy.ts

export default fromNodeMiddleware((req, res, next) => {
  console.log('Legacy middleware')
  next()
})
Never combine next() callback with a legacy middleware that is async or returns a Promise.
Server Storage
Nitro provides a cross-platform storage layer. In order to configure additional storage mount points, you can use nitro.storage, or server plugins.

Example of adding a Redis storage:

Using nitro.storage:

nuxt.config.ts

export default defineNuxtConfig({
  nitro: {
    storage: {
      redis: {
        driver: 'redis',
        /* redis connector options */
        port: 6379, // Redis port
        host: "127.0.0.1", // Redis host
        username: "", // needs Redis >= 6
        password: "",
        db: 0, // Defaults to 0
        tls: {} // tls/ssl
      }
    }
  }
})
Then in your API handler:

server/api/storage/test.ts

export default defineEventHandler(async (event) => {
  // List all keys with
  const keys = await useStorage('redis').getKeys()

  // Set a key with
  await useStorage('redis').setItem('foo', 'bar')

  // Remove a key with
  await useStorage('redis').removeItem('foo')

  return {}
})
Read more about Nitro Storage Layer.
Alternatively, you can create a storage mount point using a server plugin and runtime config:


server/plugins/storage.ts

nuxt.config.ts

import redisDriver from 'unstorage/drivers/redis'

export default defineNitroPlugin(() => {
  const storage = useStorage()

  // Dynamically pass in credentials from runtime configuration, or other sources
  const driver = redisDriver({
      base: 'redis',
      host: useRuntimeConfig().redis.host,
      port: useRuntimeConfig().redis.port,
      /* other redis connector options */
    })

  // Mount driver
  storage.mount('redis', driver)
})

---

shared
Use the shared/ directory to share functionality between the Vue app and the Nitro server.
The shared/ directory allows you to share code that can be used in both the Vue app and the Nitro server.

The shared/ directory is available in Nuxt v3.14+.
Code in the shared/ directory cannot import any Vue or Nitro code.
Usage
Method 1: Using named export

shared/utils/capitalize.ts

export const capitalize = (input: string) => {
  return input[0] ? input[0].toUpperCase() + input.slice(1) : ''
}
Method 2: Using default export

shared/utils/capitalize.ts

export default function capitalize (input: string) {
  return input[0] ? input[0].toUpperCase() + input.slice(1) : ''
}
Usage: You can now use auto-imported utility functions in .js, .ts and .vue files within your Vue app and the server/ directory.

If you have set compatibilityVersion: 4 in your nuxt.config.ts, you can use the auto-imported functions in the app/ directory. This is part of Nuxt's progressive compatibility features preparing for version 4.

app.vue

<script setup lang="ts">
const hello = capitalize('hello')
</script>

<template>
  <div>
    {{ hello }}
  </div>
</template>
server/api/hello.get.ts

export default defineEventHandler((event) => {
  return {
    hello: capitalize('hello')
  }
})
Auto Imports
Only files in the shared/utils/ and shared/types/ directories will be auto-imported. Files nested within subdirectories of these directories will not be auto-imported.

The way shared/utils and shared/types auto-imports work and are scanned is identical to the composables/ and utils/ directories.
 Read more in Docs > Guide > Directory Structure > Composables#how Files Are Scanned.
Directory Structure

-| shared/
---| capitalize.ts        # Not auto-imported
---| formatters
-----| lower.ts           # Not auto-imported
---| utils/
-----| lower.ts           # Auto-imported
-----| formatters
-------| upper.ts         # Not auto-imported
---| types/
-----| bar.d.ts           # Auto-imported
Any other files you create in the shared/ folder must be manually imported using the #shared alias (automatically configured by Nuxt):


// For files directly in the shared directory
import capitalize from '#shared/capitalize'

// For files in nested directories
import lower from '#shared/formatters/lower'

// For files nested in a folder within utils
import upper from '#shared/utils/formatters/upper'
This alias ensures consistent imports across your application, regardless of the importing file's location.

---

utils
Use the utils/ directory to auto-import your utility functions throughout your application.
The main purpose of the utils/ directory is to allow a semantic distinction between your Vue composables and other auto-imported utility functions.

Usage
Method 1: Using named export

utils/index.ts

export const { format: formatNumber } = Intl.NumberFormat('en-GB', {
  notation: 'compact',
  maximumFractionDigits: 1
})
Method 2: Using default export

utils/random-entry.ts or utils/randomEntry.ts

// It will be available as randomEntry() (camelCase of file name without extension)
export default function (arr: Array<any>) {
  return arr[Math.floor(Math.random() * arr.length)]
}
You can now use auto imported utility functions in .js, .ts and .vue files

app.vue

<template>
  <p>{{ formatNumber(1234) }}</p>
</template>
 Read more in Docs > Guide > Concepts > Auto Imports.
 Read and edit a live example in Docs > Examples > Features > Auto Imports.
The way utils/ auto-imports work and are scanned is identical to the composables/ directory.
These utils are only available within the Vue part of your app.
Only server/utils are auto-imported in the server/ directory.

---

.env
A .env file specifies your build/dev-time environment variables.
This file should be added to your .gitignore file to avoid pushing secrets to your repository.
Dev, Build and Generate Time
Nuxt CLI has built-in dotenv support in development mode and when running nuxi build and nuxi generate.

In addition to any process environment variables, if you have a .env file in your project root directory, it will be automatically loaded at dev, build and generate time. Any environment variables set there will be accessible within your nuxt.config file and modules.

.env

MY_ENV_VARIABLE=hello
Note that removing a variable from .env or removing the .env file entirely will not unset values that have already been set.
Custom File
If you want to use a different file - for example, to use .env.local or .env.production - you can do so by passing the --dotenv flag when using nuxi.

Terminal

npx nuxi dev --dotenv .env.local
When updating .env in development mode, the Nuxt instance is automatically restarted to apply new values to the process.env.

In your application code, you should use Runtime Config instead of plain env variables.
Production
After your server is built, you are responsible for setting environment variables when you run the server.

Your .env files will not be read at this point. How you do this is different for every environment.

This design decision was made to ensure compatibility across various deployment environments, some of which may not have a traditional file system available, such as serverless platforms or edge networks like Cloudflare Workers.

Since .env files are not used in production, you must explicitly set environment variables using the tools and methods provided by your hosting environment. Here are some common approaches:

You can pass the environment variables as arguments using the terminal:
$ DATABASE_HOST=mydatabaseconnectionstring node .output/server/index.mjs
You can set environment variables in shell configuration files like .bashrc or .profile.
Many cloud service providers, such as Vercel, Netlify, and AWS, provide interfaces for setting environment variables via their dashboards, CLI tools or configuration files.
Production Preview
For local production preview purpose, we recommend using nuxi preview since using this command, the .env file will be loaded into process.env for convenience. Note that this command requires dependencies to be installed in the package directory.

Or you could pass the environment variables as arguments using the terminal. For example, on Linux or macOS:

Terminal

DATABASE_HOST=mydatabaseconnectionstring node .output/server/index.mjs
Note that for a purely static site, it is not possible to set runtime configuration config after your project is prerendered.

 Read more in Docs > Guide > Going Further > Runtime Config.
If you want to use environment variables set at build time but do not care about updating these down the line (or only need to update them reactively within your app) then appConfig may be a better choice. You can define appConfig both within your nuxt.config (using environment variables) and also within an ~/app.config.ts file in your project.

---

app.vue
The app.vue file is the main component of your Nuxt application.
Minimal Usage
With Nuxt 3, the pages/ directory is optional. If not present, Nuxt won't include vue-router dependency. This is useful when working on a landing page or an application that does not need routing.

app.vue

<template>
  <h1>Hello World!</h1>
</template>
 Read and edit a live example in Docs > Examples > Hello World.
Usage with Pages
If you have a pages/ directory, to display the current page, use the <NuxtPage> component:

app.vue

<template>
  <div>
    <NuxtLayout>
      <NuxtPage/>
    </NuxtLayout>
  </div>
</template>
Since <NuxtPage> internally uses Vue's <Suspense> component, it cannot be set as a root element.
Remember that app.vue acts as the main component of your Nuxt application. Anything you add to it (JS and CSS) will be global and included in every page.
If you want to have the possibility to customize the structure around the page between pages, check out the layouts/ directory.

---

app.config.ts
Expose reactive configuration within your application with the App Config file.
Nuxt provides an app.config config file to expose reactive configuration within your application with the ability to update it at runtime within lifecycle or using a nuxt plugin and editing it with HMR (hot-module-replacement).

You can easily provide runtime app configuration using app.config.ts file. It can have either of .ts, .js, or .mjs extensions.

app.config.ts

export default defineAppConfig({
  foo: 'bar'
})
Do not put any secret values inside app.config file. It is exposed to the user client bundle.
When configuring a custom srcDir, make sure to place the app.config file at the root of the new srcDir path.
Usage
To expose config and environment variables to the rest of your app, you will need to define configuration in app.config file.

app.config.ts

export default defineAppConfig({
  theme: {
    primaryColor: '#ababab'
  }
})
We can now universally access theme both when server-rendering the page and in the browser using useAppConfig composable.

pages/index.vue

<script setup lang="ts">
const appConfig = useAppConfig()

console.log(appConfig.theme)
</script>
The updateAppConfig utility can be used to update the app.config at runtime.

pages/index.vue

<script setup>
const appConfig = useAppConfig() // { foo: 'bar' }

const newAppConfig = { foo: 'baz' }

updateAppConfig(newAppConfig)

console.log(appConfig) // { foo: 'baz' }
</script>
Read more about the updateAppConfig utility.
Typing App Config
Nuxt tries to automatically generate a TypeScript interface from provided app config so you won't have to type it yourself.

However, there are some cases where you might want to type it yourself. There are two possible things you might want to type.

App Config Input
AppConfigInput might be used by module authors who are declaring what valid input options are when setting app config. This will not affect the type of useAppConfig().

index.d.ts

declare module 'nuxt/schema' {
  interface AppConfigInput {
    /** Theme configuration */
    theme?: {
      /** Primary app color */
      primaryColor?: string
    }
  }
}

// It is always important to ensure you import/export something when augmenting a type
export {}
App Config Output
If you want to type the result of calling useAppConfig(), then you will want to extend AppConfig.

Be careful when typing AppConfig as you will overwrite the types Nuxt infers from your actually defined app config.
index.d.ts

declare module 'nuxt/schema' {
  interface AppConfig {
    // This will entirely replace the existing inferred `theme` property
    theme: {
      // You might want to type this value to add more specific types than Nuxt can infer,
      // such as string literal types
      primaryColor?: 'red' | 'blue'
    }
  }
}

// It is always important to ensure you import/export something when augmenting a type
export {}
Merging Strategy
Nuxt uses a custom merging strategy for the AppConfig within the layers of your application.

This strategy is implemented using a Function Merger, which allows defining a custom merging strategy for every key in app.config that has an array as value.

The function merger can only be used in the extended layers and not the main app.config in project.
Here's an example of how you can use:


layer/app.config.ts

app.config.ts

export default defineAppConfig({
  // Default array value
  array: ['hello'],
})
Known Limitations
As of Nuxt v3.3, the app.config.ts file is shared with Nitro, which results in the following limitations:

You cannot import Vue components directly in app.config.ts.
Some auto-imports are not available in the Nitro context.
These limitations occur because Nitro processes the app config without full Vue component support.

While it's possible to use Vite plugins in the Nitro config as a workaround, this approach is not recommended:

nuxt.config.ts

export default defineNuxtConfig({
  nitro: {
    vite: {
      plugins: [vue()]
    }
  }
})
Using this workaround may lead to unexpected behavior and bugs. The Vue plugin is one of many that are not available in the Nitro context.

---

error.vue
The error.vue file is the error page in your Nuxt application.
During the lifespan of your application, some errors may appear unexpectedly at runtime. In such case, we can use the error.vue file to override the default error files and display the error nicely.

error.vue

<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps({
  error: Object as () => NuxtError
})
</script>

<template>
  <div>
    <h1>{{ error.statusCode }}</h1>
    <NuxtLink to="/">Go back home</NuxtLink>
  </div>
</template>
Although it is called an 'error page' it's not a route and shouldn't be placed in your ~/pages directory. For the same reason, you shouldn't use definePageMeta within this page. That being said, you can still use layouts in the error file, by utilizing the NuxtLayout component and specifying the name of the layout.
The error page has a single prop - error which contains an error for you to handle.

The error object provides the following fields:


{
  statusCode: number
  fatal: boolean
  unhandled: boolean
  statusMessage?: string
  data?: unknown
  cause?: unknown
}
If you have an error with custom fields they will be lost; you should assign them to data instead:


throw createError({
  statusCode: 404,
  statusMessage: 'Page Not Found',
  data: {
    myCustomField: true
  }
})

---

nuxt.config.ts
Nuxt can be easily configured with a single nuxt.config file.
The nuxt.config file extension can either be .js, .ts or .mjs.

nuxt.config.ts

export default defineNuxtConfig({
  // My Nuxt config
})
defineNuxtConfig helper is globally available without import.
You can explicitly import defineNuxtConfig from nuxt/config if you prefer:

nuxt.config.ts

import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  // My Nuxt config
})
Discover all the available options in the Nuxt configuration documentation.
To ensure your configuration is up to date, Nuxt will make a full restart when detecting changes in the main configuration file, the .env, .nuxtignore and .nuxtrc dotfiles.

The .nuxtrc file can be used to configure Nuxt with a flat syntax. It is based on unjs/rc9.

.nuxtrc

ssr=false
If present the properties in .nuxtrc file will overwrite the properties in the nuxt.config file.

---

