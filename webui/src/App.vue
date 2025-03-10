<template>
  <div id="app">
    <h1>Hostname Generator</h1>

    <!-- Add Theme -->
    <div class="form-container">
      <input v-model="newTheme" placeholder="Theme Name" />
      <input v-model="newNames" placeholder="Comma-separated names" />
      <button @click="addTheme">Add Theme</button>
    </div>

    <h2>Themes</h2>
    <ul>
      <li v-for="theme in themes" :key="theme">
        <strong @click="fetchThemeNames(theme)">{{ theme }}</strong>
        <button @click="deleteTheme(theme)">Delete Theme</button>

        <div v-if="selectedTheme === theme">
          <h3>Names in {{ theme }}</h3>
          <ul>
            <li v-for="name in themeNames" :key="name">
              {{ name }}
              <button @click="removeName(theme, name)">❌</button>
              <button @click="editNamePrompt(theme, name)">✏️</button>
            </li>
          </ul>
          <input v-model="newName" placeholder="Add a new name" />
          <button @click="addName(theme)">➕ Add Name</button>
        </div>
      </li>
    </ul>

    <!-- Edit Name Modal -->
    <div v-if="editingName" class="modal">
      <h3>Editing: {{ editingOldName }}</h3>
      <input v-model="editingNewName" placeholder="New name" />
      <button @click="updateName()">Update</button>
      <button @click="cancelEdit()">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// Fix: Use a fallback API URL if the environment variable is undefined
const API_BASE_URL =
  import.meta.env?.VITE_API_BASE_URL || "http://localhost:8000";

export default {
  data() {
    return {
      themes: [],
      newTheme: "",
      newNames: "",
      selectedTheme: null,
      themeNames: [],
      newName: "",
      editingName: false,
      editingTheme: "",
      editingOldName: "",
      editingNewName: "",
    };
  },
  methods: {
    async fetchThemes() {
      let res = await axios.get(`${API_BASE_URL}/themes`);
      this.themes = res.data;
    },
    async fetchThemeNames(theme) {
      this.selectedTheme = theme;
      let res = await axios.get(`${API_BASE_URL}/theme/${theme}`);
      this.themeNames = res.data;
    },
    async fetchHostname(theme) {
      let res = await axios.get(`${API_BASE_URL}/${theme}`);
      alert(`Assigned hostname: ${res.data.hostname}`);
    },
    async addTheme() {
      if (!this.newTheme || !this.newNames) return;
      await axios.post(
        `${API_BASE_URL}/add_theme/${this.newTheme}`,
        this.newNames.split(","),
      );
      this.newTheme = "";
      this.newNames = "";
      this.fetchThemes();
    },
    async deleteTheme(theme) {
      await axios.delete(`${API_BASE_URL}/remove_theme/${theme}`);
      this.fetchThemes();
      if (this.selectedTheme === theme) {
        this.selectedTheme = null;
        this.themeNames = [];
      }
    },
    async addName(theme) {
      if (!this.newName) return;
      await axios.post(`${API_BASE_URL}/add_names/${theme}`, [this.newName]);
      this.newName = "";
      this.fetchThemeNames(theme);
    },
    async removeName(theme, name) {
      await axios.delete(`${API_BASE_URL}/remove_name/${theme}/${name}`);
      this.fetchThemeNames(theme);
    },
    editNamePrompt(theme, oldName) {
      this.editingName = true;
      this.editingTheme = theme;
      this.editingOldName = oldName;
      this.editingNewName = oldName;
    },
    async updateName() {
      await axios.put(
        `${API_BASE_URL}/update_name/${this.editingTheme}`,
        null,
        {
          params: {
            old_name: this.editingOldName,
            new_name: this.editingNewName,
          },
        },
      );
      this.cancelEdit();
      this.fetchThemeNames(this.editingTheme);
    },
    cancelEdit() {
      this.editingName = false;
      this.editingTheme = "";
      this.editingOldName = "";
      this.editingNewName = "";
    },
  },
  mounted() {
    this.fetchThemes();
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 20px;
}
.form-container {
  margin-bottom: 20px;
}
input {
  margin: 5px;
  padding: 8px;
}
button {
  margin: 5px;
  padding: 8px;
  cursor: pointer;
}
ul {
  list-style-type: none;
}
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid black;
  box-shadow: 0px 0px 10px gray;
}
</style>
