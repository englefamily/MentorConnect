import { createContext, useEffect, useState } from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";
import { fetch_api } from "./helpers/functions";

const context = createContext();

export default context;

export const Provider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [userData, setUserData] = useState(() =>
    localStorage.getItem("authTokens")
      ? jwt_decode(JSON.parse(localStorage.getItem("authTokens")).access)
      : null
  );
  const [loading, setLoading] = useState(true);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const navigate = useNavigate()

  useEffect(() => {
    let timeout = null;
    if (loading) {
      // updateTokens();
      setLoading(false);
    }
    if (authTokens) {
      const TimeToUpdateToken = 1000 * 60 * 4;
      timeout = setTimeout(() => {
        updateTokens();
      }, TimeToUpdateToken);
    }
    
    return () => {
      timeout && clearTimeout(timeout);
    };
  }, [authTokens, loading]);

  const loginUser = async (email, password) => {
    const data = {
      email: email,
      password: password,
    };
    console.log("🚀 ~ file: Context.js:49 ~ loginUser ~ data:", data)
    const response = await fetch_api("token", "POST", data);
    if (response.status === 200) {
      setAuthTokens(response.data);
      console.log("🚀 ~ file: Context.js:52 ~ loginUser ~ response.data:", response.data)
      setUserData(jwt_decode(response.data.access));
      localStorage.setItem("authTokens", JSON.stringify(response.data));
      console.log(jwt_decode(response.data.access));
      return { tokens: response.data };
    } else {
      return null
    }
  };

  const logoutUser = () => {
    localStorage.removeItem("authTokens");
    setAuthTokens(null);
    setUserData(null);
    window.location.reload();
  };

  const updateTokens = async () => {
    if (authTokens?.refresh) {
      const response = await fetch_api("refresh-token", "POST", {
        refresh: authTokens.refresh,
      });
      if (response.status === 200) {
        setAuthTokens(response.data);
        setUserData(jwt_decode(response.data.access));
        localStorage.setItem("authTokens", JSON.stringify(response.data));
        console.log("update token");
      } else {
        console.log("logout");
        logoutUser();
      }
    }

    if (loading) {
      setLoading(false);
    }
  };

  const contextData = {
    authTokens: authTokens,
    userData: userData,
    showLoginModal: showLoginModal,
    setAuthTokens: setAuthTokens,
    setUserData: setUserData,
    setShowLoginModal: setShowLoginModal,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  return (
    <context.Provider value={contextData}>
      {loading ? null : children}
    </context.Provider>
  );
};
