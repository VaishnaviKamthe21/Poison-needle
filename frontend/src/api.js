import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:5000" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status;
    if (status === 401 || status === 422) {
      localStorage.removeItem("token");
    }
    return Promise.reject(err);
  }
);

export default api;
