const ListdownFieldItemComponent = {
    props: ["key", "id", "data", "nameItemComponent", "value"],
    emits: ['change'],
    template: `<div v-on:click="$emit('change', id, value)">
        <component :is="nameItemComponent" v-bind="$attrs" :data=data><slot/></component>
    </div>`,
}
