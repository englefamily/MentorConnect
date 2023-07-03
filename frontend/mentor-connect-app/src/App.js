import { useContext } from "react";
import SiteRoutes from "./SiteRoute";
import BaseNavbar from "./components/BaseNavbar";
import CategorySubcategoryDropdown from "./components/CategorySubcategoryDropdown";
import NewComponent from "./components/LoginModel";
import LoginModal from "./components/modals/LoginModal";
import context from "./Context";

function App() {
  const { showLoginModal, setShowLoginModal } = useContext(context);

  return (
    <>
      <BaseNavbar />
      {showLoginModal && <LoginModal />}
      <SiteRoutes />
    </>
  );
}

export default App;
