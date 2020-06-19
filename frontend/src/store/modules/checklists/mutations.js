import { getField, updateField } from "vuex-map-fields";

export default {
  updateField,
  SET_ANSWERS (state, payload) {
    state.answers = payload
  },
  SET_LIST (state, payload) {
    state.list = payload
  },
  SET_LIST_QUESTIONS (state, payload) {
    state.list.questions = payload
  },
  SET_LISTS (state, payload) {
    state.lists = payload
  },
  SET_ENTRIES (state, payload) {
    state.entries = payload
  },
  SET_AUTOCOMPLETE (state, payload) {
    state.autocomplete = payload
  }
}
