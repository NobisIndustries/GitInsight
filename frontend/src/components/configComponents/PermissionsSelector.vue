<template>
  <v-select
      v-model="display_permission"
      :items="available_permissions"
      :disabled="disabled"
  ></v-select>
</template>

<style scoped>

</style>

<script>
export default {
  name: 'PermissionsSelector',
  props: {
    value: Object,
    disabled: Boolean,
  },
  computed: {
    display_permission: {
      get() {
        const value_key = to_sorted_json(this.value);
        for (const [permission_name, permission_content] of Object.entries(permission_mapping)) {
          if (to_sorted_json(permission_content) === value_key)
            return permission_name;
        }
        return null;
      },
      set(display_value) {
        this.$emit('input', permission_mapping[display_value])
      }
    },
    available_permissions() {
      return Object.keys(permission_mapping);
    }
  },
}

function to_sorted_json(object_to_serialize) {
  return JSON.stringify(object_to_serialize, Object.keys(object_to_serialize).sort());
}

const permission_mapping = {
  'Nothing': {view_analysis: false, edit_contributors: false, edit_all: false},
  'View Analysis': {view_analysis: true, edit_contributors: false, edit_all: false},
  'Edit Authors & Teams': {view_analysis: true, edit_contributors: true, edit_all: false},
  'Admin': {view_analysis: true, edit_contributors: true, edit_all: true},
};
</script>
