import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const STRONG_PASSWORD_REGEX =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!STRONG_PASSWORD_REGEX.test(password)) {
      setError(
        'Mật khẩu phải có tối thiểu 8 ký tự, gồm chữ hoa, chữ thường, số và một ký tự đặc biệt trong @$!%*?&.',
      );
      return;
    }

    if (password !== confirmPassword) {
      setError('Xác nhận mật khẩu không khớp.');
      return;
    }

    try {
      await axios.post(`${API_BASE_URL}/api/register`, {
        name: name.trim(),
        email: email.trim(),
        password,
      });
      navigate('/login');
    } catch (requestError) {
      setError(requestError.response?.data?.error || 'Đăng ký thất bại.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-8 border rounded shadow-sm">
      <h1 className="text-2xl font-bold mb-6 text-center">Đăng Ký Tài Khoản</h1>
      {error && (
        <div
          className="bg-red-100 text-red-700 p-3 mb-4 rounded"
          role="alert"
        >
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="register-name" className="block text-gray-700 mb-2">
            Họ Tên *
          </label>
          <input
            id="register-name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            className="w-full border p-2 rounded"
            autoComplete="name"
            required
          />
        </div>
        <div>
          <label htmlFor="register-email" className="block text-gray-700 mb-2">
            Email *
          </label>
          <input
            id="register-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full border p-2 rounded"
            autoComplete="email"
            required
          />
        </div>
        <div>
          <label
            htmlFor="register-password"
            className="block text-gray-700 mb-2"
          >
            Mật khẩu *
          </label>
          <input
            id="register-password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full border p-2 rounded"
            autoComplete="new-password"
            aria-describedby="register-password-help"
            required
          />
          <p id="register-password-help" className="text-xs text-gray-500 mt-1">
            Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và một ký tự trong
            @$!%*?&.
          </p>
        </div>
        <div>
          <label
            htmlFor="register-confirm-password"
            className="block text-gray-700 mb-2"
          >
            Xác nhận mật khẩu *
          </label>
          <input
            id="register-confirm-password"
            type="password"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            className="w-full border p-2 rounded"
            autoComplete="new-password"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Đăng Ký
        </button>

        <div className="text-center text-sm">
          Đã có tài khoản?{' '}
          <Link to="/login" className="text-blue-600 hover:underline">
            Đăng nhập
          </Link>
        </div>
      </form>
    </div>
  );
}
