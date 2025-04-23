package com.productos.service;

import com.productos.entity.Producto;
import com.productos.exception.ProductoNotFoundException;
import com.productos.repository.ProductoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
public class ProductoService {

    @Autowired
    private ProductoRepository repository;

    public Producto crear(Producto producto) {
        return repository.save(producto);
    }

    public Producto obtener(Long id) {
        return repository.findById(id).orElseThrow(() -> new ProductoNotFoundException(id));
    }

    public Producto actualizar(Long id, Producto producto) {
        if (!repository.existsById(id)) {
            throw new ProductoNotFoundException(id);
        }
        producto.setId(id);
        return repository.save(producto);
    }

    public void eliminar(Long id) {
        if (!repository.existsById(id)) {
            throw new ProductoNotFoundException(id);
        }
        repository.deleteById(id);
    }

    public Page<Producto> listar(int page, int size) {
        return repository.findAll(PageRequest.of(page, size));
    }
}


