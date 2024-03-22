const ListdownFieldComponent = {
    props: ["id", "value", "name", "edit", 'uneditableField', 'nameItemComponent'],
    emits: ['search-item', 'change', 'blur', 'focus', 'update:value', 'update:id'],
    template: `
        <div class="component_listdown">
            <span class="button_ss" @click="focus" :class="{'d-none': is_edit}">[[ mvalue ]]</span>
            <div class="form_listdown" :class="{'d-none': !is_edit}">
                <input type='text' v-model.trim="query" @keyup="search_item" @blur="blur" class="field_listdown" v-bind="$attrs">
                <div class="suggestions">
                    <listdown-field-item-component
                        @change="select_item"
                        v-for="item in item_list"
                        :data="item.data"
                        :value="item.value"
                        :key="item.id"
                        :id="item.id"
                        :name-item-component="nameItemComponent"
                    >[[item.value]]</listdown-field-item-component>
                </div>
                <input type="hidden" v-bind:name="name" v-model.trim="mid">
            </div>
        </div>
        `,
    data() {
        return {
            mvalue: this.value,
            query: '',
            mid: this.id,
            is_edit: this.edit,
            item_list: [],
            uneditable: this.uneditableField,
        }
    },
    methods: {
        focus(event) {
            if (this.uneditable) {
                return;
            }
            this.is_edit = true;
            let self = this;
            setTimeout(function() {
                if (!self.query) self.query = self.mvalue;
                self.$el.querySelector('.field_listdown').focus();
                self.$emit('focus', self);
            }, 20);
        },
        blur(event) {
            let self = this;
            setTimeout( // чтобы сначала отработало событие click на выбранном элементе
                function() {
                    self.is_edit = false;
                    self.$emit('blur', self);
                },
                100,
            );
        },
        search_item(event) {
            this.item_list = [];
            this.$emit('search-item', this);
        },
        select_item(item_id, item_value) {
            this.mid = item_id;
            this.mvalue = item_value;
            this.$emit('update:id', item_id);
            this.$emit('update:value', item_value);
            if (this.$emit('change', item_id, item_value)) {
                this.is_edit = false;
                this.query = '';
            }
        },
    },
    components: {
        ListdownFieldItemComponent
    },
}
