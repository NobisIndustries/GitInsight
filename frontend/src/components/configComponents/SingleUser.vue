<template>
  <div class="d-flex">


  </div>
</template>

<script>
export default {
  name: 'SingleUser',
  props: {
    username_init: String,
    permissions_init: Object,
    is_existing_user: {
      type: Boolean,
      required: false,
      default: false,
    },
    is_guest_user: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      editable: false,
      username: this.username_init,
      permissions: this.permissions_init,
    };
  }

}
</script>

<style scoped>

</style>