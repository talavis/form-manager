
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: "Home", component: () => import('pages/IndexPage.vue') },
    ]
  },
  {
    path: '/forms',
    component: () => import('layouts/MainLayout.vue'),
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

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
