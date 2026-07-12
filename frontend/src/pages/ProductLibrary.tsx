import { Grid, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { fetchProducts } from "../api/client";
import { EmptyState } from "../components/EmptyState";
import { ErrorAlert } from "../components/ErrorAlert";
import { LoadingState } from "../components/LoadingState";
import { ProductCard } from "../components/ProductCard";
import { ProductFilters } from "../components/ProductFilters";
import type { Product } from "../types";

export function ProductLibraryPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    fetchProducts()
      .then((items) => setProducts(items))
      .catch(() => setError("Unable to load products"))
      .finally(() => setLoading(false));
  }, []);
  return (
    <div>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Product Library
      </Typography>
      <ProductFilters />
      {loading && <LoadingState />}
      {error && <ErrorAlert message={error} />}
      {!loading && !error && products.length === 0 && (
        <EmptyState
          title="No products"
          message="No results matched your search"
        />
      )}
      <Grid container spacing={2}>
        {products.map((product) => (
          <Grid item xs={12} md={6} key={product.id}>
            <ProductCard product={product} />
          </Grid>
        ))}
      </Grid>
    </div>
  );
}
