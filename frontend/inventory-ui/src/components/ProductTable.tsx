/**
 * File: ProductTable.tsx
 * Description: Table component to list products with actions + client-side pagination.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Render product list with name, price, quantity, and updated date.
 * - Provide buttons for view, edit, and delete actions.
 * - Paginate locally when items > 5 (resets to page 1 on items change).
 *
 * Notes:
 * - Requires parent props for onEdit, onView, and admin permissions.
 */

import { useEffect, useMemo, useState } from "react";
import { useProducts } from "../store/products";
import type { ProductOut } from "../types/product";

const PAGE_SIZE = 5;

export default function ProductTable({
  items, loading, isAdmin, onEdit, onView,
}: {
  items: ProductOut[];
  loading: boolean;
  isAdmin: boolean;
  onEdit: (id: number) => void;
  onView: (id: number) => void;
}) {
  const { remove } = useProducts();

  // Pagination state
  const [page, setPage] = useState(1);
  const totalPages = Math.max(1, Math.ceil(items.length / PAGE_SIZE));

  // Reset to first page when items change
  useEffect(() => {
    setPage(1);
  }, [items]);

  const pageItems = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return items.slice(start, start + PAGE_SIZE);
  }, [items, page]);

  const showPager = items.length > PAGE_SIZE;

  // simple page buttons (windowed)
  const pagesToShow = useMemo(() => {
    const maxButtons = 5;
    if (totalPages <= maxButtons) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }
    // window around current page
    const half = Math.floor(maxButtons / 2);
    let start = Math.max(1, page - half);
    let end = Math.min(totalPages, start + maxButtons - 1);
    // adjust start if near the end
    start = Math.max(1, end - maxButtons + 1);
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }, [page, totalPages]);

  const startIdx = (page - 1) * PAGE_SIZE + 1;
  const endIdx = Math.min(page * PAGE_SIZE, items.length);

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full">
        <thead className="bg-gray-100 text-left">
          <tr>
            <th className="p-3">Image</th>
            <th className="p-3">Name</th>
            <th className="p-3">Price</th>
            <th className="p-3">Qty</th>
            <th className="p-3">Updated</th>
            <th className="p-3"></th>
          </tr>
        </thead>
        <tbody>
          {loading && <tr><td className="p-4" colSpan={6}>Loading...</td></tr>}
          {!loading && items.length === 0 && (
            <tr><td className="p-4 text-gray-500" colSpan={6}>No products found</td></tr>
          )}
          {!loading && pageItems.map((p) => (
            <tr key={p.id} className="border-t">
              <td className="p-3">
                {p.image_url ? (
                  <img src={p.image_url} alt={p.name} className="w-12 h-12 object-cover rounded-lg" />
                ) : (
                  <div className="w-12 h-12 bg-gray-200 rounded-lg grid place-items-center text-xs text-gray-500">no img</div>
                )}
              </td>
              <td className="p-3">{p.name}</td>
              <td className="p-3">${Number(p.price ?? 0).toFixed(2)}</td>
              <td className="p-3">{p.quantity}</td>
              <td className="p-3">{new Date(p.updated_at).toLocaleString()}</td>
              <td className="p-3">
                <div className="flex gap-3">
                  <button className="text-gray-700 hover:underline" onClick={() => onView(p.id)}>View</button>
                  {isAdmin && (
                    <>
                      <button className="text-blue-600 hover:underline" onClick={() => onEdit(p.id)}>Edit</button>
                      <button className="text-red-600 hover:underline" onClick={() => remove(p.id)}>Delete</button>
                    </>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Paginator */}
      {showPager && (
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-3 border-t bg-white">
          <div className="text-sm text-gray-600">
            Showing <span className="font-medium">{startIdx}</span>–<span className="font-medium">{endIdx}</span> of <span className="font-medium">{items.length}</span>
          </div>

          <div className="flex items-center gap-1">
            <button
              className="px-3 py-1.5 rounded-lg border disabled:opacity-50"
              onClick={() => setPage(1)}
              disabled={page === 1}
            >
              « First
            </button>
            <button
              className="px-3 py-1.5 rounded-lg border disabled:opacity-50"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              ‹ Prev
            </button>

            {pagesToShow.map((n) => (
              <button
                key={n}
                className={`px-3 py-1.5 rounded-lg border ${n === page ? "bg-black text-white border-black" : "bg-white"}`}
                onClick={() => setPage(n)}
              >
                {n}
              </button>
            ))}

            <button
              className="px-3 py-1.5 rounded-lg border disabled:opacity-50"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
            >
              Next ›
            </button>
            <button
              className="px-3 py-1.5 rounded-lg border disabled:opacity-50"
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages}
            >
              Last »
            </button>
          </div>
        </div>
      )}
    </div>
  );
}