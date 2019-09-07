<template lang="pug">
    form(@submit.prevent='sendChecklist')
        .checklist__info__wrap
            .checklist__info
                .info__id
                    span.info__id__text &CHcy;&iecy;&kcy;&lcy;&icy;&scy;&tcy; &numero; {{list.id}}
                .info__name
                    h2.info__name__text {{list.name}}
                .info__description
                    p.info__description__text {{list.description}}
            fieldset(v-for='question in list.questions')
                div(v-if="question.type === 'textarea'")
                    label(for='textarea') {{question.text}}
                    textarea#textarea(
                        :type='question.type'
                        name='textarea'
                        placeholder='Введите текст ...'
                        )
                div(v-else-if="question.type === 'radio'")
                    legend {{question.text}}
                    div(v-for="choice in question.choices.split(';')")
                        input#radio1(
                            type='radio'
                            name='radios'
                            :value='choice'
                            v-model='answers[question.id]'
                            )
                        label(for='radio1') {{choice}}
                        br
                div(v-else-if="question.type === 'select-multiple'")
                    legend {{question.text}}
                    div(v-for="(choice, id) in question.choices.split(';')")
                        input(
                            type='checkbox'
                            :id="'check'+ id"
                            :value="choice"
                            name='checkboxes'
                            v-model='test'
                            @change="answers[question.id] = test.join(';')"
                            )
                        label(:for="'check'+ id") {{choice}}
                        br
                div(v-else-if="question.type === 'select-image'")
                    div(v-if="!answers[question.id]")
                        h2 Select an image
                        input(
                            type="file"
                            @change="onFileChange($event, question.id)"
                            )
                    div(v-else)
                        img(
                            :src="image"
                            )
                        button(
                            @click="removeImage(question.id)"
                            ) Remove image
                    br
                div(v-else='')
                    label(for='firstName') {{question.text}}
                    input#firstName(
                        v-model='answers[question.id]'
                        :type='question.type'
                        name='name'
                        placeholder='Введите текст ...'
                        )
            button Отправить
            | {{list}}
            br
            | {{answers}}
            br
            | {{test}}
</template>

<script>
    import { mapState } from 'vuex';

    export default {
        name: "checklist",
        data() {
            return {
                test: [],
                image: "",
                answers: {
                },
            }
        },
        created: function () {
            this.$store.dispatch('list', this.$route.params.id);
        },
        computed: {
            ...mapState(["list"])
        },
        methods: {
            sendChecklist() {
                this.$store.commit('SET_ANSWERS', this.answers);
                this.$store.dispatch('create_list', this.$route.params.id);
            },
            onFileChange(e, id) {
                console.log(e);
                console.log(id);
                let files = e.target.files || e.dataTransfer.files;
                if (!files.length) return;
                this.createImage(files[0], id);
            },
            createImage(file, id) {
                let reader = new FileReader();
                reader.onload = e => {
                    this.image = e.target.result;
                    this.answers[id] = e.target.result;
                };
                reader.readAsDataURL(file);
            },
            removeImage(id) {
                this.answers[id] = "";
                this.image = "";
            }
        }
    }
</script>

<style lang="sass" scoped>
    img
        width: 100%

    form
        max-width: 300px
        background: #FFFFFF
        padding: 10px 20px

    fieldset
        margin: 0 0 1rem 0
        padding: 0
        border: none

    legend
        font-weight: 400
        display: inline-block
        margin-bottom: .5rem

    label
        display: inline-block
        margin-bottom: .5rem

    input[type='text'], textarea, select
        display: block
        padding: .5rem
        width: 100%
        background-color: white
        border-radius: .25rem
        border: 1px solid #e5e5e5
        outline: none
        transition-property: none
        transition-duration: inherit

        &:focus
            border-color: #2980B9

    textarea
        max-width: 300px
        height: 100px

    input[type='text'], select
        height: 34px

    select
        font-size: .875rem

    input[type='checkbox'], input[type='radio']
            position: relative
            top: 5px
            width: 22px
            height: 22px
            margin: 0 .5rem
            background-color: white
            border: 1px solid #e5e5e5
            outline: none
            -moz-appearance: none
            -webkit-appearance: none
            /* List some properties that might change
            transition-property: none
            transition-duration: inherit
    input[type='checkbox']
        border-radius: 5px
        &:checked
            background-color: #2980B9
            border: none
            &:after
                display: block
                content: ''
                height: 8px
                width: 10px
                border-bottom: 3px solid #fff
                border-left: 3px solid #fff
                transform: translate(5px, 6px) rotate(-45deg) scale(1)
    input[type='radio']
        border-radius: 50%
        &:checked
            border-width: 5px
            border-color: white
            background-color: #2980B9

    button
        display: block
        margin: 1em auto
        padding: .5rem 2rem
        font-size: 125%
        color: white
        border: none
        border-radius: .25rem
        background-color: #2980B9
        outline: none
        box-shadow: 0 0.4rem 0.1rem -0.3rem rgba(0, 0, 0, 0.1)
        /* We'll talk about this next
        transform: perspective(300px) scale(0.95) translateZ(0)
        transform-style: preserve-3d
        /* List the properties that you're looking to transition.
         * Try not to use 'all'
        transition-property: none
        /* This applies to all of the above properties
        transition-duration: inherit
        &:hover
            cursor: pointer
            background-color: #2980B9
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0)
            transform: scale(1.1) rotateX(0)
        &:active
            background-color: #2980B9
            transform: scale(1.05) rotateX(-10deg)
</style>