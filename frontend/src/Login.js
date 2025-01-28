import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link, BrowserRouter as Router, Route, Routes } from "react-router-dom";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    // Dummy authentication logic
    if (username && password) {
      onLogin();
    } else {
      alert("Please enter valid credentials");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Card className="w-96 p-4">
        <CardContent>
          <h1 className="text-xl font-bold mb-4">Login</h1>
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mb-4"
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mb-4"
          />
          <Button onClick={handleLogin} className="w-full">
            Login
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

const Header = () => (
  <header className="p-4 bg-gray-800 text-white flex justify-between">
    <h1 className="text-lg font-bold">FastAPI Query App</h1>
    <nav>
      <Link to="/dashboard" className="mr-4">Dashboard</Link>
      <Link to="/query">Query</Link>
    </nav>
  </header>
);

const Sidebar = () => (
  <aside className="w-64 p-4 bg-gray-200 min-h-screen">
    <ul>
      <li className="mb-2">
        <Link to="/dashboard">Home</Link>
      </li>
      <li>
        <Link to="/query">Query</Link>
      </li>
    </ul>
  </aside>
);

const Dashboard = () => (
  <div className="p-4">
    <h2 className="text-xl font-bold">Dashboard</h2>
    <p>Welcome to the dashboard!</p>
  </div>
);

const QueryPage = () => (
  <div className="p-4">
    <h2 className="text-xl font-bold">Query Page</h2>
    <p>Build your query page here.</p>
  </div>
);

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Header />
          <main className="p-4">
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/query" element={<QueryPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
