<template>
<q-page class="flex flex-center">
  <q-card class="bg-grey-2">
    <q-card-section class="bg-primary text-white">
      <div class="text-h6">Form Manager Login</div>
    </q-card-section>
    <q-form
      @submit="doLogin"
      class="q-gutter-md"
    >
      <q-card-section class="rows">	
	<q-input name="email" v-model="email" label="Email" />
      </q-card-section>
      <q-card-actions align="right">
	<q-btn color="primary" label="Submit" type="submit"/>
      </q-card-actions>
    </q-form>
  </q-card>
</q-page>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'IndexPage',
  data () {
    return {
      email: "",
      error: false,
    }
  },
  methods: {
    doLogin() {
      axios
	.post('/api/v1/user/login', {"email": this.email})
        .then((response) => {
	  this.$router.push({ name: 'FormBrowser'});
        resolve(response);
      })
      .catch((err) => {
	this.error = true;
      });

    }
  }
})
</script>
