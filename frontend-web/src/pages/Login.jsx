import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Đăng nhập thất bại. Vui lòng kiểm tra lại.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    // Simulated Google OAuth login
    alert('Tính năng tích hợp Google OAuth đang được mô phỏng cho môi trường kiểm thử.');
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm">
      <h2 className="text-2xl font-bold mb-6 text-center">Đăng nhập</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700 mb-2">
            Email <span className="text-red-500">*</span>
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 mb-2">
            Mật khẩu <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border p-2 rounded pr-16"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 text-gray-500 hover:text-gray-700 font-medium"
            >
              {showPassword ? 'Ẩn' : 'Hiện'}
            </button>
          </div>
        </div>

        <div className="text-right text-sm -mt-2">
          <a href="/forgot-password" className="text-blue-500 hover:underline">Quên mật khẩu?</a>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
          disabled={isLoading}
          tabIndex={1}
        >
          {isLoading ? 'Đang đăng nhập...' : 'Đăng nhập'}
        </button>

        {/* Google OAuth Login Button */}
        <div className="mt-4">
          <button
            type="button"
            onClick={handleGoogleLogin}
            className="w-full border border-gray-300 text-gray-700 py-2 rounded hover:bg-gray-50 flex items-center justify-center gap-2 transition-colors"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.53-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.66-5.17 3.66-8.17z"
              />
              <path
                fill="#34A853"
                d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.11 0-5.74-2.11-6.68-4.96H1.21v3.15C3.18 21.88 7.39 24 12 24z"
              />
              <path
                fill="#FBBC05"
                d="M5.32 14.24A7.16 7.16 0 0 1 5 12c0-.79.13-1.57.32-2.34V6.51H1.21A11.94 11.94 0 0 0 0 12c0 1.92.45 3.74 1.21 5.49l4.11-3.25z"
              />
              <path
                fill="#EA4335"
                d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.39 0 3.18 2.12 1.21 5.69l4.11 3.25c.94-2.85 3.57-4.96 6.68-4.96z"
              />
            </svg>
            Đăng nhập bằng Google
          </button>
        </div>

        <div className="text-center text-sm mt-2">
          Chưa có tài khoản? <Link to="/register" className="text-blue-600 hover:underline">Đăng ký ngay</Link>
        </div>
      </form>

      {error && <div className="bg-red-100 text-red-700 p-3 mt-4 rounded text-sm">{error}</div>}
    </div>
  );
}
