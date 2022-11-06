<template>
  <div id="content-wrapper">
    <router-view></router-view>
  </div>
</template>

<script>

  export default {
    data() {
      return {
        menuItems: [
          // {
          //   key:'map',
          //   title: 'Map',
          //   icon: './assets/map-marker.svg',
          //   alt: 'Map Icon',
          //   link: '/',
          // },
          // {
          //   key:'profile',
          //   title: 'Profile',
          //   icon: './assets/user.svg',
          //   alt: 'Profile Icon',
          //   link: 'profile',
          // },
        ],
        // pageTitle: 'Map'
      };
    },
    mounted() {}
  }

</script>

<style scoped>

</style>
