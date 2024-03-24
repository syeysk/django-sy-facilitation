const StepMemberItemComponent = {
    props: ['member', 'memberMode'],
    data() {
        return {
            mode: this.memberMode || 'view',
            previous_for_what: undefined,
            uneditable_invited: this.memberMode != 'add',
            bad_message: '',
            STATIC_PREFIX,
            CURRENT_USERNAME,
        };
    },
    template: `
        <tr>
            <td>
                <listdown-field-component
                      @search-item="search_user"
                      @change="select_user"
                      @blur="blur_selecting_user"
                      @focus="focus_selecting_user"
                      v-model:value="member.invited"
                      :edit="member.edit"
                      name="invited"
                      :uneditable-field="uneditable_invited"
                      placeholder="логин участника"
                      name-item-component="member-search-item-component"
                ></listdown-field-component>
            </td>
            <td>
                <span>
                    <span class="el_sign" style="display: inline-block; width: 100%;" :class="{'d-none': !(mode == 'view')}">[[ member.for_what ]]</span>
                    <input v-model.trim="member.for_what" name="for_what" class="el_field" :class="{'d-none': !(mode == 'edit' || mode == 'add')}" placeholder="цель приглашения"/>
                </span>
            </td>
            <!--<td>[[ member.inviting ]]</td>-->
            <td style="text-align: center;">
                <svg class="bi member-icon icon-positive" role="img" title="Save" @click="save" :class="{'d-none': !(mode == 'edit' || mode == 'add')}">
                    <use :xlink:href="STATIC_PREFIX + 'base/extern/bootstrap-icons.svg#check-square-fill'"/>
                </svg>
                <svg v-if="member.inviting == CURRENT_USERNAME" class="bi member-icon icon-neutral" role="img" title="Edit" @click="edit" :class="{'d-none': !(mode == 'view')}">
                    <use :xlink:href="STATIC_PREFIX + 'base/extern/bootstrap-icons.svg#pencil-fill'"/>
                </svg>
                <svg class="bi member-icon icon-negative" role="img" title="Cancel" @click="cancel" :class="{'d-none': !(mode == 'edit' || mode == 'add')}">
                    <use :xlink:href="STATIC_PREFIX + 'base/extern/bootstrap-icons.svg#x-square-fill'"/>
                </svg>
            </td>
        </tr>
        <tr :class="{'d-none': !bad_message}">
            <td colspan="3">
                <div class="alert alert-danger" role="alert">[[ bad_message ]]</div>
            </td>
        </tr>`,
    components: {
        ListdownFieldComponent,
    },
    methods: {
        save(component) {
            let self = this;
            $.ajax({
                url: URL_FACI_EDITOR_MEMBER,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {for_what: self.member.for_what, invited_user: self.member.invited, mode: self.mode},
                success: function(result) {
                    open_block(result['open_block']);
                    self.$parent.mode = 'view';
                    self.mode = 'view';
                    self.uneditable_invited = true;
                    self.bad_message = '';
                },
                statusCode: {
                    400: function(xhr) {
                        self.bad_message = ''
                        for (let key in xhr.responseJSON) {
                            self.bad_message += key + ': ' + xhr.responseJSON[key] + '';
                        }
                    },
                    403: function(xhr) {
                        self.bad_message = xhr.responseJSON;
                    }
                },
                method: "post"
            });
        },
        search_user(component) {
            $.ajax({
                url: URL_SEARCH_USER,
                headers: {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                dataType: 'json',
                data: {search_string: component.query},
                success: function(result) {
                    let username;
                    for (user_data of result) {
                        component.item_list.push({'id': user_data.username, 'value': user_data.username, 'data': user_data});
                    }
                    if (component.item_list.length == 0) {
                        component.item_list.push({'id': null, 'value': 'пользователь не найден', 'data': {'last_name': 'пользователь не найден'}});
                    }
                },
                method: "post"
            });
        },
        select_user(id, value) {
        },
        blur_selecting_user(component) {
        },
        focus_selecting_user(component) {
        },
        edit() {
            this.$parent.mode = 'edit';
            this.mode = 'edit';
            this.previous_for_what = this.member.for_what;
        },
        cancel() {
            if (this.mode == 'add') {
                this.$parent.member_list.pop(-1);
            }
            this.$parent.mode = 'view';
            this.mode = 'view';
            this.member.for_what = this.previous_for_what;
            this.bad_message = '';
        },
    },
}
