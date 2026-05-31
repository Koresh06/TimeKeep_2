export default function Spinner() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '40px 0' }}>
      <div
        style={{
          width: 32,
          height: 32,
          border: '3px solid rgba(200,30,30,0.15)',
          borderTopColor: '#c81e1e',
          borderRadius: '50%',
          animation: 'mchs-spin 0.7s linear infinite',
        }}
      />
      <style>{`@keyframes mchs-spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}
