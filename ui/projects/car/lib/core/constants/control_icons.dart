class ControlIcons {
  static const String engineControl = '''
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Common engine/start button symbol: Power symbol with ring -->
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
      <path d="M12 6v12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M12 6a6 6 0 0 1 0 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  ''';

  static const String doorLock = '''
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Car with lock symbol -->
      <path d="M17 12H7c-.55 0-1 .45-1 1v2c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-2c0-.55-.45-1-1-1zm-1 2H8v-1h8v1z" fill="currentColor"/>
      <path d="M18 10h-1V7c0-2.21-1.79-4-4-4h-2C8.79 3 7 4.79 7 7v3H6c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-7c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM9 7c0-1.1.9-2 2-2h2c1.1 0 2 .9 2 2v3H9V7z" fill="currentColor"/>
    </svg>
  ''';

  static const String climateControl = '''
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- AC/Fan symbol commonly used in cars -->
      <circle cx="12" cy="12" r="3" fill="currentColor"/>
      <path d="M12 5v2M12 17v2M5 12h2M17 12h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M7.05 7.05l1.41 1.41M15.54 15.54l1.41 1.41M7.05 16.95l1.41-1.41M15.54 8.46l1.41-1.41" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z" fill="currentColor"/>
    </svg>
  ''';
}