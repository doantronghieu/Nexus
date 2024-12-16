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
  <!-- Outer circle -->
  <circle cx="12" cy="12" r="10" fill="#4A5568" opacity="0.1"/>
  
  <!-- Temperature display background -->
  <rect x="8" y="6" width="8" height="12" rx="4" fill="#4A5568"/>
  
  <!-- Temperature "mercury" tube -->
  <rect x="10" y="8" width="4" height="8" rx="2" fill="#E2E8F0"/>
  
  <!-- Air flow indicators -->
  <path d="M4 12h2M18 12h2M12 4v2M12 18v2" 
        stroke="#48BB78" 
        stroke-width="1.5" 
        stroke-linecap="round"/>
  
  <!-- Temperature markers -->
  <path d="M16 8h1M16 10h1M16 12h1M16 14h1" 
        stroke="#E2E8F0" 
        stroke-width="0.5"/>
        
  <!-- Plus/Minus controls -->
  <circle cx="12" cy="18.5" r="1" fill="#48BB78"/>
  <path d="M12 18h2M11 18.5h2" stroke="#E2E8F0" stroke-width="0.5"/>
  <circle cx="12" cy="5.5" r="1" fill="#48BB78"/>
  <path d="M11 5.5h2" stroke="#E2E8F0" stroke-width="0.5"/>
  
  <text x="12" y="22" 
        font-family="Arial, sans-serif" 
        font-size="2.5" 
        text-anchor="middle" 
        fill="#2D3748">
    CLIMATE
  </text>
</svg>''';
}
