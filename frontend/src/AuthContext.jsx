import React from "react";
import api from "./api";

export const AuthContext = React.createContext({ user: null, loading: true, login: async()=>{}, logout: ()=>{} });

export function AuthProvider({ children }) {
  const [state, setState] = React.useState({ user: null, loading: true });

  const fetchMe = React.useCallback(async () => {
    try {
      const r = await api.get("/auth/me");
      setState({ user: r.data.user, loading: false });
    } catch {
      localStorage.removeItem("token");
      setState({ user: null, loading: false });
    }
  }, []);

  React.useEffect(() => { fetchMe(); }, [fetchMe]);

  const login = async (email, password) => {
    const r = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", r.data.access_token);
    await fetchMe();
  };

  const logout = () => {
    localStorage.removeItem("token");
    setState({ user: null, loading: false });
  };

  return (
    <AuthContext.Provider value={{ user: state.user, loading: state.loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
