<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Form Manager
        </q-toolbar-title>

        <q-btn
	  flat
	  round
	  type="a"
	  href="/api/v1/user/logout"
	  v-if="userStore.email !== ''"
	  icon="logout"
	  />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useUserStore } from 'stores/user'

export default defineComponent({
  name: 'MainLayout',
  setup() {
    const userStore = useUserStore()

    return { userStore }
  },
})
</script>
