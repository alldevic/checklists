<template lang="pug">
    v-container(
        class="fill-height"
        fluid
    )
        v-row(
            align="center"
            justify="center"
        )
            v-col(
                cols="12"
                sm="8"
                md="4"
            )
                v-card(class="elevation-2 rounded-card" tile)
                    v-toolbar(
                        color="primary"
                        dark
                        flat
                    )
                        v-toolbar-title Введите свои данные
                        div(class="flex-grow-1")
                    v-card-text(class="px-6 pt-6 pb-0")
                        ValidationObserver(v-slot="{ passes }")
                            form(@keyup.enter="onSubmit")
                                ValidationProvider(name="почта" rules="required|email" v-slot="{ errors }")
                                    v-text-field(
                                        :error-messages="errors"
                                        v-model="email"
                                        label="Почта"
                                        :prepend-icon="mdiEmail"
                                    )
                                ValidationProvider(name="пароль" rules="required|min:8" v-slot="{ errors }")
                                    v-text-field(
                                        :error-messages="errors"
                                        v-model="password"
                                        id="password"
                                        label="Пароль"
                                        name="password"
                                        :prepend-icon="mdiLock"
                                        type="password"
                                    )
                    v-card-actions(class="justify-end px-6")
                        v-btn(class="ma-2" tile outlined color="primary" @click="clear") Очистить
                        v-btn(tile color="primary" @click="onSubmit") Войти
</template>

<script>
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapActions } from 'vuex'

import {
  mdiEmail,
  mdiLock
} from '@mdi/js'

export default {
  name: 'Login',
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data: () => ({
    mdiEmail,
    mdiLock,
    email: '',
    password: ''
  }),
  computed: {},
  methods: {
    ...mapActions({
      LOGIN: 'user/LOGIN'
    }),
    onSubmit () {
      this.LOGIN({
        email: this.email,
        password: this.password
      })
    },
    clear () {
      this.email = ''
      this.password = ''
    }
  }
}
</script>
