
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { 'loginRequired': true },
    children: [
      { path: '', name: "FormBrowser", component: () => import('pages/FormBrowser.vue')},
      {
	path: 'responses/:identifier',
	name: "FormResponses",
	component: () => import('pages/FormResponses.vue'),
	props: route => ({'identifier': route.params.identifier})
      }
    ]
  },

  {
    path: '/login',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: "Login", component: () => import('pages/LoginPage.vue') },
    ]
  },

  {
    path: '/error',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: "Error", component: () => import('pages/Error.vue') },
    ],
    props: route => ({'message': route.params.message})
  },

  
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
