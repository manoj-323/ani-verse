import {
  createBrowserRouter,
  Route,
  RouterProvider,
  createRoutesFromElements,
} from "react-router-dom";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import "./index.css";
import App from "./App.jsx";
import Home from "./components/Home/Home.jsx";
import About from "./components/About/About.jsx";
import Login from "./components/Login/Login.jsx";
import Search from "./components/Search/Search.jsx";
import Explore from "./components/Explore/Explore.jsx";
import Profile from "./components/Profile/Profile.jsx";
import Contact from "./components/Contact/Contact.jsx";
import NotFound from "./components/NotFound/NotFound.jsx";
import Recommendation from "./components/Recommendation/Recommendation.jsx";


const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />}>
      <Route path="" element={<Home />} />
      <Route path="*" element={<NotFound />} />
      <Route path="about" element={<About />} />
      <Route path="login" element={<Login />} />
      <Route path="search" element={<Search />} />
      <Route path="profile" element={<Profile />} />
      <Route path="contact" element={<Contact />} />
      <Route path="explore" element={<Explore />} />
      <Route path="recommendation" element={<Recommendation />} />
    </Route>
  )
);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);