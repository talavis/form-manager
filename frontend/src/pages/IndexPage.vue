<template>
<q-page class="flex flex-center">
  <q-btn label="login" type="a" href="/api/v1/user/login" text-color="primary"/>
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
      })
      .catch((err) => {
	this.error = true;
      });

    }
  }
})
</script>
