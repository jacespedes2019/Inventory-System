/**
 * File: ProductDetailModal.tsx
 * Description: Modal to display detailed information about a product.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Show product details including image, description, price, quantity, updated date.
 * - Provide close action.
 *
 * Notes:
 * - Read-only view, does not allow editing.
 * - Requires product object passed from parent.
 */
import type { ProductOut } from "../types/product";

export default function ProductDetailModal({
  open,
  onClose,
  product,
}: {
  open: boolean;
  onClose: () => void;
  product: ProductOut | null;
}) {
  if (!open || !product) return null;

  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/40">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="text-lg font-semibold">Product details</h3>
          <button className="text-gray-500" onClick={onClose}>✕</button>
        </div>

        <div className="grid md:grid-cols-2 gap-0">
          <div className="p-4 border-b md:border-b-0 md:border-r">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-64 object-cover rounded-xl"
              />
            ) : (
              <div className="w-full h-64 grid place-items-center rounded-xl bg-gray-100 text-gray-500">
                No image
              </div>
            )}
          </div>
          <div className="p-6 space-y-3">
            <div>
              <div className="text-sm text-gray-500">Name</div>
              <div className="text-base font-medium">{product.name}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Description</div>
              <div className="text-base">{product.description || "-"}</div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-gray-500">Price</div>
                <div className="text-base font-medium">${Number(product.price ?? 0).toFixed(2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Quantity</div>
                <div className="text-base font-medium">{product.quantity}</div>
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Updated at</div>
              <div className="text-base">{new Date(product.updated_at).toLocaleString()}</div>
            </div>
          </div>
        </div>

        <div className="p-4 border-t flex justify-end">
          <button className="rounded-lg border px-4 py-2" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}