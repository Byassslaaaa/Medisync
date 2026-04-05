package grpcclient

// codec.go — workaround untuk file .pb.go yang ditulis manual tanpa
// full protobuf descriptor. Codec ini mengganti codec "proto" default
// gRPC dengan JSON agar serialization/deserialization tetap berfungsi.
//
// Dalam proyek nyata (generate via protoc), file ini tidak diperlukan.

import (
	"encoding/json"

	"google.golang.org/grpc/encoding"
)

func init() {
	encoding.RegisterCodec(jsonGRPCCodec{})
}

type jsonGRPCCodec struct{}

func (jsonGRPCCodec) Marshal(v interface{}) ([]byte, error) {
	return json.Marshal(v)
}

func (jsonGRPCCodec) Unmarshal(data []byte, v interface{}) error {
	return json.Unmarshal(data, v)
}

// Name HARUS "proto" agar menimpa codec default gRPC.
func (jsonGRPCCodec) Name() string { return "proto" }
