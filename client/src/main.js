import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue'
import 'bootstrap/dist/css/bootstrap.css';
import App from './App.vue'
import router from './router'
import VuePlyr from 'vue-plyr'
import 'vue-plyr/dist/vue-plyr.css'


Vue.use(BootstrapVue);
Vue.use(VuePlyr, 
  {
    plyr: {}
  })

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
