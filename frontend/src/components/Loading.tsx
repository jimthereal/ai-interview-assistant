export default function Loading({ text = 'Loading...' }: { text?: string }) {
  return (
    <div className="flex items-center justify-center p-12">
      <div className="text-center">
        <div className="spinner mx-auto mb-4"></div>
        <p className="text-[var(--text-secondary)]">{text}</p>
      </div>
    </div>
  );
}
