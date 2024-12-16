class ControlIcons {
  static const String engineControl = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M7 4v2h3v2H7l-2 2v3H3v-3H1v8h2v-3h2v3h3l2 2h8v-4h2v3h3V9h-3v3h-2V8h-6V6h3V4H7z" fill="#4A5568" class="base"/>
  <circle cx="18" cy="17" r="1.5" fill="#48BB78"/>
  <path d="M17.5 14.5v2" stroke="#48BB78" stroke-width="1" stroke-linecap="round"/>
  <text x="12" y="22" font-family="Arial, sans-serif" font-size="2.5" text-anchor="middle" fill="#2D3748">ENGINE START</text>
</svg>''';

  static const String doorLock = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <rect x="7" y="11" width="10" height="8" rx="1" fill="#4A5568"/>
  <path d="M9 11V7a3 3 0 0 1 6 0v4" fill="none" stroke="#4A5568" stroke-width="2" stroke-linecap="round"/>
  <circle cx="12" cy="15" r="1" fill="#E2E8F0"/>
  <text x="12" y="22" font-family="Arial, sans-serif" font-size="2.5" text-anchor="middle" fill="#2D3748">DOOR LOCK</text>
</svg>''';

  static const String climateControl = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <rect x="6" y="6" width="12" height="12" rx="2" fill="#4A5568"/>
  <path d="M11 8v6.5a1.5 1.5 0 1 0 2 0V8" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M4 12h3M17 12h3M12 4v3M12 17v3" stroke="#48BB78" stroke-width="1.5" stroke-linecap="round"/>
  <text x="12" y="22" font-family="Arial, sans-serif" font-size="2.5" text-anchor="middle" fill="#2D3748">CLIMATE</text>
</svg>''';
}
